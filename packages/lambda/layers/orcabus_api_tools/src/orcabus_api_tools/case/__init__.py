#!/usr/bin/env python3

"""Case service toolkit for querying cases and linking external entities."""

# Standard imports
from typing import Dict, Optional

# Local imports
from ..utils.requests_helpers import (
    get_request,
    get_request_response_results,
    get_url,
    post_request,
)
from .globals import CASE_SUBDOMAIN_NAME


def get_case_url(endpoint: str) -> str:
    """
    Get the base URL for the case api
    :param endpoint:
    :return:
    """
    return get_url(
        endpoint,
        CASE_SUBDOMAIN_NAME
    )


def get_case_request(
        endpoint: str,
        params: Optional[Dict] = None,
):
    """Execute an authenticated GET request to the case service.

    Args:
        endpoint: The API endpoint path.
        params: Optional query parameters.

    Returns:
        The parsed JSON response.
    """
    return get_request(get_case_url(endpoint), params=params)


def get_case_request_response_results(
        endpoint: str,
        params: Optional[Dict] = None,
):
    """Execute a paginated GET request to the case service.

    Args:
        endpoint: The API endpoint path.
        params: Optional query parameters.

    Returns:
        A list of all results across all pages.
    """
    return get_request_response_results(get_case_url(endpoint), params=params)


def case_post_request(
        endpoint: str,
        json_data: Optional[Dict] = None,
) -> Dict:
    """Execute an authenticated POST request to the case service.

    Args:
        endpoint: The API endpoint path.
        json_data: Optional JSON body data.

    Returns:
        The parsed JSON response.
    """
    return post_request(
        get_case_url(endpoint),
        json_data=json_data,
    )


from .case_helpers import (
    list_cases,
    get_case,
    link_entity_to_case,
    sync_case_from_redcap,
)

__all__ = [
    # Get helpers
    "list_cases",
    "get_case",
    # Post helpers
    "link_entity_to_case",
    "sync_case_from_redcap",
]
