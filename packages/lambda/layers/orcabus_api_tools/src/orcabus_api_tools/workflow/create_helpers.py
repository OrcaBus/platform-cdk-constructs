#!/usr/bin/env python4

"""
Create helpers
"""

# Standard imports
from datetime import datetime, timezone
import random
from typing import Optional

# Local imports
from orcabus_api_tools.workflow.globals import WORKFLOW_RUN_PREFIX


def generate_rand_hex_string(length: int = 8) -> str:
    """
    Generate a random hexadecimal string of a given length.
    :param length: Length of the hexadecimal string to generate.
    :return: Random hexadecimal string.
    """
    return ''.join(random.choices('0123456789abcdef', k=length))


def create_portal_run_id():
    """Generate a unique portal run ID combining today's date with a random hex string.

    Returns:
        A portal run ID string in the format 'YYYYMMDDxxxxxxxx'.
    """
    return datetime.now(timezone.utc).strftime("%Y%m%d") + str(generate_rand_hex_string())[0:8]


def create_workflow_run_name_from_workflow_name_workflow_version_and_portal_run_id(
        workflow_name: str,
        workflow_version: str,
        portal_run_id: str,
        workflow_run_prefix: Optional[str] = None
):
    """Generate a standardized workflow run name.

    Args:
        workflow_name: The workflow name.
        workflow_version: The workflow version string.
        portal_run_id: The portal run identifier.
        workflow_run_prefix: Optional custom prefix. Defaults to WORKFLOW_RUN_PREFIX.

    Returns:
        A workflow run name in the format 'prefix--name--version--portalRunId'.
    """
    return '--'.join([
        (
            WORKFLOW_RUN_PREFIX
            if workflow_run_prefix is None
            else workflow_run_prefix
        ),
        workflow_name.lower(),
        workflow_version.replace(".", "-"),
        portal_run_id
    ])