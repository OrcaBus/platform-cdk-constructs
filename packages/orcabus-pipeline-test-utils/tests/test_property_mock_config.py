"""Property-based tests for MockConfigBuilder structural integrity.

# Feature: deployment-integration-tests, Property 7: MockConfigBuilder Structural Integrity

Validates: Requirements 5.6

For any set of state machine names, test case names (unique per state machine),
state-to-mock mappings, and mocked response definitions, the `MockConfigBuilder.build()`
output SHALL produce valid MockConfigFile JSON containing all specified state machines,
all specified test cases within each state machine, and all specified mocked responses.
"""

from __future__ import annotations

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from orcabus_pipeline_test_utils.sfn_local.mock_config import MockConfigBuilder


# --- Strategies ---

# Generate valid names (non-empty, alphanumeric with limited special chars)
name_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="_-"),
    min_size=1,
    max_size=30,
).filter(lambda s: s.strip() != "")

# Generate simple JSON-serializable response payloads
json_value_strategy = st.recursive(
    st.one_of(
        st.none(),
        st.booleans(),
        st.integers(min_value=-1000, max_value=1000),
        st.text(min_size=0, max_size=20),
    ),
    lambda children: st.one_of(
        st.lists(children, max_size=3),
        st.dictionaries(
            st.text(min_size=1, max_size=10),
            children,
            max_size=3,
        ),
    ),
    max_leaves=5,
)


@st.composite
def mocked_response_entry(draw: st.DrawFn) -> dict[str, dict]:
    """Strategy to generate a valid mocked response dict (index -> Return/Throw)."""
    num_invocations = draw(st.integers(min_value=1, max_value=3))
    responses = {}
    for i in range(num_invocations):
        is_throw = draw(st.booleans())
        if is_throw:
            error_type = draw(name_strategy)
            cause = draw(st.text(min_size=1, max_size=30))
            responses[str(i)] = {"Throw": {"Error": error_type, "Cause": cause}}
        else:
            payload = draw(json_value_strategy)
            responses[str(i)] = {"Return": payload}
    return responses


@st.composite
def mock_config_inputs(draw: st.DrawFn) -> dict:
    """Strategy to generate a full set of MockConfigBuilder inputs.

    Returns a dict with:
    - state_machines: list of unique state machine names
    - test_cases: dict mapping sm_name -> list of (test_case_name, state_mocks) tuples
    - mocked_responses: dict mapping response_name -> responses dict
    """
    # Generate 1-4 state machines
    num_sms = draw(st.integers(min_value=1, max_value=4))
    sm_names = draw(
        st.lists(name_strategy, min_size=num_sms, max_size=num_sms, unique=True)
    )

    # Generate mocked response names (shared pool across all test cases)
    num_responses = draw(st.integers(min_value=1, max_value=6))
    response_names = draw(
        st.lists(
            name_strategy, min_size=num_responses, max_size=num_responses, unique=True
        )
    )
    # Ensure response names don't collide with state machine names (not required by schema
    # but helps clarity)

    # Generate response definitions
    mocked_responses = {}
    for resp_name in response_names:
        mocked_responses[resp_name] = draw(mocked_response_entry())

    # Generate test cases per state machine
    test_cases: dict[str, list[tuple[str, dict[str, str]]]] = {}
    for sm_name in sm_names:
        num_tcs = draw(st.integers(min_value=1, max_value=3))
        tc_names = draw(
            st.lists(name_strategy, min_size=num_tcs, max_size=num_tcs, unique=True)
        )
        tcs = []
        for tc_name in tc_names:
            # Generate state-to-mock mappings (1-4 task states per test case)
            num_mappings = draw(st.integers(min_value=1, max_value=4))
            task_state_names = draw(
                st.lists(
                    name_strategy,
                    min_size=num_mappings,
                    max_size=num_mappings,
                    unique=True,
                )
            )
            # Map each task state to a randomly chosen response name
            state_mocks = {}
            for task_name in task_state_names:
                resp_name = draw(st.sampled_from(response_names))
                state_mocks[task_name] = resp_name
            tcs.append((tc_name, state_mocks))
        test_cases[sm_name] = tcs

    return {
        "state_machines": sm_names,
        "test_cases": test_cases,
        "mocked_responses": mocked_responses,
    }


# --- Property Tests ---


class TestPropertyMockConfigBuilderStructuralIntegrity:
    """Property-based tests for MockConfigBuilder.build() structural integrity.

    **Validates: Requirements 5.6**
    """

    @settings(max_examples=100)
    @given(inputs=mock_config_inputs())
    def test_all_state_machines_present_in_output(self, inputs: dict):
        """All specified state machine names appear in the build output."""
        builder = MockConfigBuilder()

        for sm_name in inputs["state_machines"]:
            builder.add_state_machine(sm_name)

        for sm_name, tcs in inputs["test_cases"].items():
            for tc_name, state_mocks in tcs:
                builder.add_test_case(sm_name, tc_name, state_mocks)

        for resp_name, responses in inputs["mocked_responses"].items():
            builder.add_mocked_response(resp_name, responses)

        output = builder.build()

        assert "StateMachines" in output
        for sm_name in inputs["state_machines"]:
            assert sm_name in output["StateMachines"], (
                f"State machine '{sm_name}' not found in output"
            )

    @settings(max_examples=100)
    @given(inputs=mock_config_inputs())
    def test_all_test_cases_present_per_state_machine(self, inputs: dict):
        """All specified test cases appear within their respective state machine."""
        builder = MockConfigBuilder()

        for sm_name in inputs["state_machines"]:
            builder.add_state_machine(sm_name)

        for sm_name, tcs in inputs["test_cases"].items():
            for tc_name, state_mocks in tcs:
                builder.add_test_case(sm_name, tc_name, state_mocks)

        for resp_name, responses in inputs["mocked_responses"].items():
            builder.add_mocked_response(resp_name, responses)

        output = builder.build()

        for sm_name, tcs in inputs["test_cases"].items():
            sm_output = output["StateMachines"][sm_name]
            assert "TestCases" in sm_output
            for tc_name, _ in tcs:
                assert tc_name in sm_output["TestCases"], (
                    f"Test case '{tc_name}' not found in state machine '{sm_name}'"
                )

    @settings(max_examples=100)
    @given(inputs=mock_config_inputs())
    def test_all_state_mocks_preserved_in_test_cases(self, inputs: dict):
        """State-to-mock mappings are preserved exactly in each test case."""
        builder = MockConfigBuilder()

        for sm_name in inputs["state_machines"]:
            builder.add_state_machine(sm_name)

        for sm_name, tcs in inputs["test_cases"].items():
            for tc_name, state_mocks in tcs:
                builder.add_test_case(sm_name, tc_name, state_mocks)

        for resp_name, responses in inputs["mocked_responses"].items():
            builder.add_mocked_response(resp_name, responses)

        output = builder.build()

        for sm_name, tcs in inputs["test_cases"].items():
            for tc_name, state_mocks in tcs:
                actual_mocks = output["StateMachines"][sm_name]["TestCases"][tc_name]
                assert actual_mocks == state_mocks, (
                    f"State mocks mismatch for '{sm_name}/{tc_name}': "
                    f"expected {state_mocks}, got {actual_mocks}"
                )

    @settings(max_examples=100)
    @given(inputs=mock_config_inputs())
    def test_all_mocked_responses_present_in_output(self, inputs: dict):
        """All specified mocked responses appear in the build output."""
        builder = MockConfigBuilder()

        for sm_name in inputs["state_machines"]:
            builder.add_state_machine(sm_name)

        for sm_name, tcs in inputs["test_cases"].items():
            for tc_name, state_mocks in tcs:
                builder.add_test_case(sm_name, tc_name, state_mocks)

        for resp_name, responses in inputs["mocked_responses"].items():
            builder.add_mocked_response(resp_name, responses)

        output = builder.build()

        assert "MockedResponses" in output
        for resp_name in inputs["mocked_responses"]:
            assert resp_name in output["MockedResponses"], (
                f"Mocked response '{resp_name}' not found in output"
            )

    @settings(max_examples=100)
    @given(inputs=mock_config_inputs())
    def test_mocked_response_content_preserved(self, inputs: dict):
        """Mocked response definitions are preserved exactly in the output."""
        builder = MockConfigBuilder()

        for sm_name in inputs["state_machines"]:
            builder.add_state_machine(sm_name)

        for sm_name, tcs in inputs["test_cases"].items():
            for tc_name, state_mocks in tcs:
                builder.add_test_case(sm_name, tc_name, state_mocks)

        for resp_name, responses in inputs["mocked_responses"].items():
            builder.add_mocked_response(resp_name, responses)

        output = builder.build()

        for resp_name, expected_responses in inputs["mocked_responses"].items():
            actual_responses = output["MockedResponses"][resp_name]
            assert actual_responses == expected_responses, (
                f"Mocked response content mismatch for '{resp_name}': "
                f"expected {expected_responses}, got {actual_responses}"
            )

    @settings(max_examples=100)
    @given(inputs=mock_config_inputs())
    def test_output_has_correct_top_level_structure(self, inputs: dict):
        """The build output always has exactly 'StateMachines' and 'MockedResponses' keys."""
        builder = MockConfigBuilder()

        for sm_name in inputs["state_machines"]:
            builder.add_state_machine(sm_name)

        for sm_name, tcs in inputs["test_cases"].items():
            for tc_name, state_mocks in tcs:
                builder.add_test_case(sm_name, tc_name, state_mocks)

        for resp_name, responses in inputs["mocked_responses"].items():
            builder.add_mocked_response(resp_name, responses)

        output = builder.build()

        assert set(output.keys()) == {"StateMachines", "MockedResponses"}

    @settings(max_examples=100)
    @given(inputs=mock_config_inputs())
    def test_no_extra_state_machines_in_output(self, inputs: dict):
        """The output contains no state machines beyond those specified."""
        builder = MockConfigBuilder()

        for sm_name in inputs["state_machines"]:
            builder.add_state_machine(sm_name)

        for sm_name, tcs in inputs["test_cases"].items():
            for tc_name, state_mocks in tcs:
                builder.add_test_case(sm_name, tc_name, state_mocks)

        for resp_name, responses in inputs["mocked_responses"].items():
            builder.add_mocked_response(resp_name, responses)

        output = builder.build()

        assert set(output["StateMachines"].keys()) == set(inputs["state_machines"])

    @settings(max_examples=100)
    @given(inputs=mock_config_inputs())
    def test_no_extra_mocked_responses_in_output(self, inputs: dict):
        """The output contains no mocked responses beyond those specified."""
        builder = MockConfigBuilder()

        for sm_name in inputs["state_machines"]:
            builder.add_state_machine(sm_name)

        for sm_name, tcs in inputs["test_cases"].items():
            for tc_name, state_mocks in tcs:
                builder.add_test_case(sm_name, tc_name, state_mocks)

        for resp_name, responses in inputs["mocked_responses"].items():
            builder.add_mocked_response(resp_name, responses)

        output = builder.build()

        assert set(output["MockedResponses"].keys()) == set(
            inputs["mocked_responses"].keys()
        )
