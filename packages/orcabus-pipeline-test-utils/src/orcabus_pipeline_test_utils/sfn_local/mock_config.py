"""MockConfigFile builder.

Fluent builder for MockConfigFile.json structure supporting:
- add_state_machine()
- add_test_case()
- add_mocked_response()
- build() and write() methods

Supports both Return and Throw mocked responses following the
AWS Step Functions Local MockConfigFile schema.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class MockConfigBuilder:
    """Fluent builder for MockConfigFile.json.

    Builds the structure expected by Step Functions Local:
    {
        "StateMachines": {
            "<name>": {
                "TestCases": {
                    "<test_case>": {
                        "<TaskState>": "<MockedResponseName>"
                    }
                }
            }
        },
        "MockedResponses": {
            "<name>": {
                "0": { "Return": {...} }
            }
        }
    }
    """

    def __init__(self) -> None:
        self._state_machines: dict[str, dict[str, dict[str, str]]] = {}
        self._mocked_responses: dict[str, dict[str, dict[str, Any]]] = {}

    def add_state_machine(self, name: str) -> MockConfigBuilder:
        """Register a state machine by name.

        Args:
            name: The state machine name (must be non-empty).

        Returns:
            self for fluent chaining.

        Raises:
            ValueError: If name is empty.
        """
        if not name:
            raise ValueError("State machine name must not be empty")
        if name not in self._state_machines:
            self._state_machines[name] = {}
        return self

    def add_test_case(
        self,
        state_machine: str,
        test_case: str,
        state_mocks: dict[str, str],
    ) -> MockConfigBuilder:
        """Add a test case to a state machine.

        Args:
            state_machine: Name of the state machine (must already be added).
            test_case: Name of the test case (must be non-empty).
            state_mocks: Mapping of task state names to mocked response names.

        Returns:
            self for fluent chaining.

        Raises:
            ValueError: If state_machine has not been added, or test_case is empty.
        """
        if not test_case:
            raise ValueError("Test case name must not be empty")
        if state_machine not in self._state_machines:
            raise ValueError(
                f"State machine '{state_machine}' not found. "
                f"Call add_state_machine('{state_machine}') first."
            )
        self._state_machines[state_machine][test_case] = dict(state_mocks)
        return self

    def add_mocked_response(
        self,
        name: str,
        responses: dict[str, dict[str, Any]],
    ) -> MockConfigBuilder:
        """Add a mocked response definition.

        Args:
            name: The mocked response name (must be non-empty).
            responses: Mapping of invocation index (as string, e.g. "0", "1")
                to response definition. Each response must contain either
                a "Return" key or a "Throw" key.

        Returns:
            self for fluent chaining.

        Raises:
            ValueError: If name is empty or any response lacks Return/Throw.
        """
        if not name:
            raise ValueError("Mocked response name must not be empty")
        for idx, response in responses.items():
            if "Return" not in response and "Throw" not in response:
                raise ValueError(
                    f"Mocked response '{name}' at index '{idx}' must contain "
                    f"either 'Return' or 'Throw' key."
                )
        self._mocked_responses[name] = dict(responses)
        return self

    def build(self) -> dict[str, Any]:
        """Return the complete MockConfigFile structure as a dict.

        Returns:
            Dict matching the MockConfigFile.json schema with
            "StateMachines" and "MockedResponses" top-level keys.
        """
        state_machines: dict[str, Any] = {}
        for sm_name, test_cases in self._state_machines.items():
            state_machines[sm_name] = {"TestCases": dict(test_cases)}

        return {
            "StateMachines": state_machines,
            "MockedResponses": dict(self._mocked_responses),
        }

    def write(self, path: str) -> None:
        """Write the MockConfigFile to a JSON file.

        Creates parent directories if they don't exist.

        Args:
            path: File path to write the JSON output to.
        """
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(self.build(), indent=2) + "\n",
            encoding="utf-8",
        )
