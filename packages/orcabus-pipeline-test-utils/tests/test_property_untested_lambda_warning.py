"""Property-based tests for untested Lambda warning completeness.

# Feature: deployment-integration-tests, Property 1: Untested Lambda Warning Completeness

Validates: Requirements 1.7

For any set of Lambda module directories and corresponding test files, the warning
output SHALL list exactly those Lambda modules that have no matching
`test_{module_name}.py` file, and no others.
"""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st


# --- Core Logic Under Test ---

# Extracted from the reference service conftest.py at
# service-dragen-wgts-dna-pipeline-manager/conftest.py
# This is the pure-function equivalent of the untested Lambda detection logic.

EXCLUDED_DIRS = {"tests", "__pycache__"}


def find_lambda_modules(directory_names: list[str]) -> list[str]:
    """Find Lambda module directory names from a list of directory names.

    A Lambda module directory ends in '_py' and is not in the excluded set.
    Returns sorted list of matching directory names.
    """
    return sorted(
        name
        for name in directory_names
        if name.endswith("_py") and name not in EXCLUDED_DIRS
    )


def find_untested_modules(
    lambda_modules: list[str],
    test_file_names: set[str],
) -> list[str]:
    """Determine which Lambda modules have no corresponding test file.

    Convention: directory `foo_bar_py` -> expected test file `test_foo_bar.py`
    (strip the `_py` suffix to get module_name, then expect `test_{module_name}.py`)

    Args:
        lambda_modules: List of Lambda module directory names (ending in _py).
        test_file_names: Set of test file names present in the tests directory.

    Returns:
        List of Lambda module directory names that have no matching test file.
    """
    untested = []
    for module_dir_name in lambda_modules:
        module_name = module_dir_name.removesuffix("_py")
        expected_test_file = f"test_{module_name}.py"
        if expected_test_file not in test_file_names:
            untested.append(module_dir_name)
    return untested


# --- Strategies ---

# Lambda module names must end in _py, be non-empty before the suffix,
# and use valid filesystem characters (snake_case convention).
lambda_module_name_strategy = st.from_regex(
    r"[a-z][a-z0-9_]{0,29}_py",
    fullmatch=True,
).filter(lambda s: s not in EXCLUDED_DIRS)

# Non-lambda directory names (don't end in _py, or are excluded)
non_lambda_dir_strategy = st.one_of(
    # Directories that don't end in _py
    st.from_regex(r"[a-z][a-z0-9_]{0,20}", fullmatch=True).filter(
        lambda s: not s.endswith("_py")
    ),
    # Excluded directories
    st.sampled_from(["tests", "__pycache__"]),
)


@st.composite
def lambda_modules_and_test_files(draw: st.DrawFn) -> tuple[list[str], set[str], set[str]]:
    """Generate a set of Lambda modules, some with test files, some without.

    Returns:
        (all_directory_names, test_file_names, expected_untested_module_names)
    """
    # Generate Lambda module directories
    num_modules = draw(st.integers(min_value=0, max_value=15))
    lambda_modules = draw(
        st.lists(
            lambda_module_name_strategy,
            min_size=num_modules,
            max_size=num_modules,
            unique=True,
        )
    )

    # Generate some non-lambda directories to mix in
    num_non_lambda = draw(st.integers(min_value=0, max_value=5))
    non_lambda_dirs = draw(
        st.lists(
            non_lambda_dir_strategy,
            min_size=num_non_lambda,
            max_size=num_non_lambda,
        )
    )

    # Decide which Lambda modules are tested (have a matching test file)
    tested_mask = draw(
        st.lists(
            st.booleans(),
            min_size=len(lambda_modules),
            max_size=len(lambda_modules),
        )
    )

    # Build test file names for tested modules
    test_file_names: set[str] = set()
    expected_untested: set[str] = set()
    for module_dir_name, is_tested in zip(lambda_modules, tested_mask):
        module_name = module_dir_name.removesuffix("_py")
        if is_tested:
            test_file_names.add(f"test_{module_name}.py")
        else:
            expected_untested.add(module_dir_name)

    # Add some spurious test files that don't correspond to any module
    num_spurious = draw(st.integers(min_value=0, max_value=3))
    spurious_test_files = draw(
        st.lists(
            st.from_regex(r"test_[a-z][a-z0-9_]{0,20}\.py", fullmatch=True),
            min_size=num_spurious,
            max_size=num_spurious,
        )
    )
    # Only add spurious files that don't accidentally match a real module
    real_test_names = {
        f"test_{m.removesuffix('_py')}.py" for m in lambda_modules
    }
    for f in spurious_test_files:
        if f not in real_test_names:
            test_file_names.add(f)

    all_dirs = lambda_modules + non_lambda_dirs
    return all_dirs, test_file_names, expected_untested


# --- Property Tests ---


class TestPropertyUntestedLambdaWarningCompleteness:
    """Property-based tests for untested Lambda warning detection.

    **Validates: Requirements 1.7**
    """

    @settings(max_examples=100)
    @given(data=lambda_modules_and_test_files())
    def test_untested_modules_are_exactly_those_without_test_files(
        self, data: tuple[list[str], set[str], set[str]]
    ):
        """The untested list contains exactly those modules with no matching test file,
        and no others."""
        all_dirs, test_file_names, expected_untested = data

        # Step 1: Extract Lambda modules from all directories
        lambda_modules = find_lambda_modules(all_dirs)

        # Step 2: Determine untested modules
        untested = find_untested_modules(lambda_modules, test_file_names)

        # Assert: untested set matches expected
        assert set(untested) == expected_untested, (
            f"Expected untested={expected_untested}, got={set(untested)}.\n"
            f"Lambda modules={lambda_modules}, test_files={test_file_names}"
        )

    @settings(max_examples=100)
    @given(data=lambda_modules_and_test_files())
    def test_untested_modules_is_subset_of_lambda_modules(
        self, data: tuple[list[str], set[str], set[str]]
    ):
        """Every module in the untested list is a valid Lambda module."""
        all_dirs, test_file_names, _ = data

        lambda_modules = find_lambda_modules(all_dirs)
        untested = find_untested_modules(lambda_modules, test_file_names)

        # All untested modules must be in the Lambda modules list
        assert set(untested).issubset(set(lambda_modules)), (
            f"Untested modules {set(untested)} not a subset of "
            f"lambda modules {set(lambda_modules)}"
        )

    @settings(max_examples=100)
    @given(data=lambda_modules_and_test_files())
    def test_tested_modules_not_in_untested_list(
        self, data: tuple[list[str], set[str], set[str]]
    ):
        """Modules that have a corresponding test file never appear in the untested list."""
        all_dirs, test_file_names, _ = data

        lambda_modules = find_lambda_modules(all_dirs)
        untested = find_untested_modules(lambda_modules, test_file_names)

        # Verify no tested module appears in untested
        for module_dir_name in lambda_modules:
            module_name = module_dir_name.removesuffix("_py")
            expected_test = f"test_{module_name}.py"
            if expected_test in test_file_names:
                assert module_dir_name not in untested, (
                    f"Module '{module_dir_name}' has test file '{expected_test}' "
                    f"but appears in untested list"
                )

    @settings(max_examples=100)
    @given(
        lambda_modules=st.lists(
            lambda_module_name_strategy,
            min_size=1,
            max_size=10,
            unique=True,
        )
    )
    def test_all_modules_untested_when_no_test_files(self, lambda_modules: list[str]):
        """When no test files exist, all Lambda modules are reported as untested."""
        sorted_modules = find_lambda_modules(lambda_modules)
        untested = find_untested_modules(sorted_modules, set())

        assert set(untested) == set(sorted_modules), (
            f"Expected all modules untested with empty test set, "
            f"got untested={set(untested)}, modules={set(sorted_modules)}"
        )

    @settings(max_examples=100)
    @given(
        lambda_modules=st.lists(
            lambda_module_name_strategy,
            min_size=1,
            max_size=10,
            unique=True,
        )
    )
    def test_no_modules_untested_when_all_have_test_files(self, lambda_modules: list[str]):
        """When every Lambda module has a corresponding test file, untested list is empty."""
        sorted_modules = find_lambda_modules(lambda_modules)

        # Create test files for all modules
        test_file_names = {
            f"test_{m.removesuffix('_py')}.py" for m in sorted_modules
        }

        untested = find_untested_modules(sorted_modules, test_file_names)

        assert untested == [], (
            f"Expected no untested modules when all have tests, "
            f"got untested={untested}"
        )

    @settings(max_examples=100)
    @given(
        dirs=st.lists(
            non_lambda_dir_strategy,
            min_size=0,
            max_size=10,
        )
    )
    def test_excluded_and_non_py_dirs_never_appear(self, dirs: list[str]):
        """Directories not ending in _py or in the excluded set are never Lambda modules."""
        lambda_modules = find_lambda_modules(dirs)

        for module in lambda_modules:
            assert module.endswith("_py"), (
                f"Module '{module}' doesn't end with '_py'"
            )
            assert module not in EXCLUDED_DIRS, (
                f"Module '{module}' is in excluded set"
            )
