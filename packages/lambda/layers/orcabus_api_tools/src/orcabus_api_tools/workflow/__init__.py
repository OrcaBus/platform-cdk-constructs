#!/usr/bin/env python3

# Typing
from typing import Optional, Dict

# Local imports
from ..utils.requests_helpers import (
    get_url, get_request,
    get_request_response_results,
    patch_request, post_request
)
from .globals import WORKFLOW_SUBDOMAIN_NAME


# Get url for the subdomain
def get_workflow_url(endpoint: str) -> str:
    """
    Get the URL for the FastQ subdomain endpoint.
    :param endpoint: The specific API endpoint for the FastQ subdomain.
    :return: The full URL for the FastQ subdomain endpoint.
    """
    return get_url(
        endpoint=endpoint,
        subdomain=WORKFLOW_SUBDOMAIN_NAME,
    )


# Wrappers
def get_workflow_request(
        endpoint: str,
        params: Optional[Dict] = None,
):
    return get_request(
        url=get_workflow_url(endpoint),
        params=params
    )


def get_workflow_request_response_results(
        endpoint: str,
        params: Optional[Dict] = None,
):
    return get_request_response_results(
        url=get_workflow_url(endpoint),
        params=params
    )


def workflow_patch_request(
    endpoint: str,
    params: Optional[Dict] = None,
):
    return patch_request(
        url=get_workflow_url(endpoint),
        params=params
    )


def workflow_post_request(
    endpoint: str,
    params: Optional[Dict] = None,
):
    return post_request(
        url=get_workflow_url(endpoint),
        params=params
    )


# Create imports
from .create_helpers import (
    create_portal_run_id,
    create_workflow_run_name_from_workflow_name_workflow_version_and_portal_run_id,
)

# Metadata helpers
from .metadata_helpers import (
    get_workflows_from_library_id
)

# Payload helpers
from .payload_helpers import (
    get_payload,
    get_payload_from_state,
    get_latest_payload_from_workflow_run,
    get_latest_payload_from_portal_run_id
)

# Workflow run helpers
from .workflow_run_helpers import (
    get_workflow_run,
    get_workflow_run_from_portal_run_id,
    get_workflow_run_state,
)

__all__ = [
    # Create helpers
    "create_portal_run_id",
    "create_workflow_run_name_from_workflow_name_workflow_version_and_portal_run_id",

    # Metadata helpers
    "get_workflows_from_library_id",

    # Payload helpers
    "get_payload",
    "get_payload_from_state",
    "get_latest_payload_from_workflow_run",
    "get_latest_payload_from_portal_run_id",

    # Workflow run helpers
    "get_workflow_run",
    "get_workflow_run_from_portal_run_id",
    "get_workflow_run_state",
]

