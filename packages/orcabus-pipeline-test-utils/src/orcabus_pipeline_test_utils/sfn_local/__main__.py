"""Entry point for `python -m orcabus_pipeline_test_utils.sfn_local.runner`.

Enables the CLI runner to be invoked as:
    python3.14 -m orcabus_pipeline_test_utils.sfn_local.runner \
        --mock-config app/step-functions-templates/tests/mocks/ \
        --tests app/step-functions-templates/tests/ \
        --timeout 180
"""

import sys

from orcabus_pipeline_test_utils.sfn_local.runner import run

if __name__ == "__main__":
    sys.exit(run())
