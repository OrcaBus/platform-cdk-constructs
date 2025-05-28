#!/usr/bin/env python3

"""
Create helper functions for the project.
"""

from uuid import uuid4
from datetime import datetime, timezone

from .globals import WORKFLOW_RUN_NAME_PREFIX


def create_portal_run_id():
    """
    Create a unique identifier for a portal run.

    Returns:
        str: A unique identifier in the format 'portal_run_<uuid>'.
    """
    return datetime.now(timezone.utc).strftime("%Y%m%d") + hex(hash(str(uuid4())))[-8:]


def create_workflow_run_name_from_workflow_name_workflow_version_and_portal_run_id(
        workflow_name: str,
        workflow_version: str,
        portal_run_id: str
) -> str:
    """
    Create a workflow run name from the workflow name and version.

    Args:
        workflow_name (str): The name of the workflow.
        workflow_version (str): The version of the workflow.
        portal_run_id (str): The portal run identifier

    Returns:
        str: A formatted string combining the workflow name and version.
    """
    return "--".join([
        *WORKFLOW_RUN_NAME_PREFIX,
        workflow_name.replace('.', '-').replace('_', '-'),
        workflow_version.replace('.', '-').replace('_', '-'),
        portal_run_id
    ])
