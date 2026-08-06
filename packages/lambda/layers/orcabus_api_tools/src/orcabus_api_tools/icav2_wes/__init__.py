#!/usr/bin/env python3

"""ICAv2 WES (Workflow Execution Service) toolkit for launching and managing ICAv2 analyses."""

# Imports
from typing import Optional, Dict

from .globals import ICAV2_WES_SUBDOMAIN_NAME
from .models import WESPostRequest
from ..utils.requests_helpers import (
    get_request, get_url, patch_request, get_request_response_results, post_request
)


# Wrappers
def get_icav2_wes_url(endpoint: str) -> str:
    """Get the URL for the ICAv2 WES service endpoint.

    Args:
        endpoint: The API endpoint path.

    Returns:
        The fully qualified URL for the endpoint.
    """
    return get_url(
        endpoint=endpoint,
        subdomain=ICAV2_WES_SUBDOMAIN_NAME,
    )


def get_icav2_wes_request(
        endpoint: str,
        params: Optional[Dict] = None,
):
    """Execute an authenticated GET request to the ICAv2 WES service.

    Args:
        endpoint: The API endpoint path.
        params: Optional query parameters.

    Returns:
        The parsed JSON response.
    """
    return get_request(
        url=get_icav2_wes_url(endpoint),
        params=params
    )


def get_icav2_wes_request_response_results(
        endpoint: str,
        params: Optional[Dict] = None,
):
    """Execute a paginated GET request to the ICAv2 WES service.

    Args:
        endpoint: The API endpoint path.
        params: Optional query parameters.

    Returns:
        A list of all results across all pages.
    """
    return get_request_response_results(
        url=get_icav2_wes_url(endpoint),
        params=params
    )


def icav2_wes_patch_request(
    endpoint: str,
    json_data: Optional[Dict] = None,
):
    """Execute an authenticated PATCH request to the ICAv2 WES service.

    Args:
        endpoint: The API endpoint path.
        json_data: Optional JSON body data.

    Returns:
        The parsed JSON response.
    """
    return patch_request(
        url=get_icav2_wes_url(endpoint),
        json_data=json_data
    )


def icav2_wes_post_request(
    endpoint: str,
    json_data: Dict
):
    """Execute an authenticated POST request to the ICAv2 WES service.

    Args:
        endpoint: The API endpoint path.
        json_data: JSON body data (required).

    Returns:
        The parsed JSON response.
    """
    # Confirm param keys are valid
    return post_request(
        url=get_icav2_wes_url(endpoint),
        json_data=json_data
    )


# Set all
from .create_helpers import create_icav2_wes_analysis
from .query_helpers import get_icav2_wes_analysis_by_name
from .update_helpers import update_icav2_wes_analysis_status

__all__ = [
    # Models
    'WESPostRequest',
    # Launch helpers
    'create_icav2_wes_analysis',
    # Query helpers
    'get_icav2_wes_analysis_by_name',
    # Update helpers
    'update_icav2_wes_analysis_status'
]
