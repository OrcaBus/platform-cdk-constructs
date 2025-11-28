#!/usr/bin/env python3
from typing import Optional, Dict

from orcabus_api_tools.utils.requests_helpers import get_url, get_request_response_results, get_request
from orcabus_api_tools.workflow.globals import WORKFLOW_SUBDOMAIN_NAME


def get_workflow_url(endpoint: str) -> str:
    """
    Get the URL for the Metadata endpoint
    :param endpoint:
    :return:
    """
    return get_url(
        endpoint,
        WORKFLOW_SUBDOMAIN_NAME
    )


def get_workflow_request(
        endpoint: str,
        params: Optional[Dict] = None,
):
    return get_request(get_workflow_url(endpoint), params=params)


def get_workflow_request_response_results(
        endpoint: str,
        params: Optional[Dict] = None,
):
    return get_request_response_results(get_workflow_url(endpoint), params=params)


# Now 'import all'
from .create_helpers import (
    create_portal_run_id,
    create_workflow_run_name_from_workflow_name_workflow_version_and_portal_run_id,
)

from .metadata_helpers import (
    get_workflows_from_library_id,
    get_workflows_from_library_id_list,
    get_workflow_runs_from_metadata,
)

from .query_helpers import (
    get_workflow_by_workflow_name,
    get_workflows_from_analysis_run_id,
    list_workflow_runs_by_workflow_name,
    list_workflow_runs_from_analysis_run_id,
    list_workflow_runs,
)

from .workflow_helpers import (
    list_workflows,
)

from .payload_helpers import (
    get_payload,
    get_payload_from_state_orcabus_id,
    get_latest_payload_from_workflow_run,
    get_latest_payload_from_portal_run_id,
)

from .workflow_run_helpers import (
    get_workflow_run,
    get_workflow_run_from_portal_run_id,
    get_workflow_run_state,
    get_workflow_run_state_from_state_orcabus_id,
)


__all__ = [
    # Create
    "create_portal_run_id",
    "create_workflow_run_name_from_workflow_name_workflow_version_and_portal_run_id",
    # Metadata
    "get_workflows_from_library_id",
    "get_workflows_from_library_id_list",
    "get_workflow_runs_from_metadata",
    # Query
    # Deprecated
    "get_workflow_by_workflow_name",
    "get_workflows_from_analysis_run_id",
    "list_workflow_runs_by_workflow_name",
    # New
    "list_workflow_runs",
    "list_workflow_runs_from_analysis_run_id",
    # Payload
    "get_payload",
    "get_payload_from_state_orcabus_id",
    "get_latest_payload_from_workflow_run",
    "get_latest_payload_from_portal_run_id",
    # Workflow
    "list_workflows",
    # Workflow Run
    "get_workflow_run",
    "get_workflow_run_from_portal_run_id",
    "get_workflow_run_state",
    "get_workflow_run_state_from_state_orcabus_id"
]
