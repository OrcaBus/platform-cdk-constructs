#!/usr/bin/env python3

"""Fastq unarchiving service toolkit for managing S3 Glacier restore jobs."""

# Standard imports
from typing import Dict, Optional

# Local imports
from .globals import FASTQ_UNARCHIVING_SUBDOMAIN_NAME
from ..utils.requests_helpers import (
    get_request_response_results,
    get_url,
    patch_request,
    get_request, post_request
)


# Get url for the subdomain
def get_fastq_unarchiving_url(endpoint: str) -> str:
    """Get the full URL for the fastq unarchiving service endpoint.

    Args:
        endpoint: The API endpoint path.

    Returns:
        The full URL for the fastq unarchiving service.
    """
    return get_url(
        endpoint=endpoint,
        subdomain=FASTQ_UNARCHIVING_SUBDOMAIN_NAME,
    )


# Wrappers
def get_fastq_unarchiving_request(
        endpoint: str,
        params: Optional[Dict] = None,
):
    """Execute an authenticated GET request to the fastq unarchiving service.

    Args:
        endpoint: The API endpoint path.
        params: Optional query parameters.

    Returns:
        The parsed JSON response.
    """
    return get_request(
        url=get_fastq_unarchiving_url(endpoint),
        params=params
    )


def get_fastq_unarchiving_request_response_results(
        endpoint: str,
        params: Optional[Dict] = None,
):
    """Execute a paginated GET request to the fastq unarchiving service.

    Args:
        endpoint: The API endpoint path.
        params: Optional query parameters.

    Returns:
        A list of all results across all pages.
    """
    return get_request_response_results(
        url=get_fastq_unarchiving_url(endpoint),
        params=params
    )


def fastq_unarchiving_patch_request(
    endpoint: str,
    json_data: Optional[Dict] = None,
):
    """Execute an authenticated PATCH request to the fastq unarchiving service.

    Args:
        endpoint: The API endpoint path.
        json_data: Optional JSON body data.

    Returns:
        The parsed JSON response.
    """
    return patch_request(
        url=get_fastq_unarchiving_url(endpoint),
        json_data=json_data
    )


def fastq_unarchiving_post_request(
    endpoint: str,
    json_data: Optional[Dict] = None,
):
    """Execute an authenticated POST request to the fastq unarchiving service.

    Args:
        endpoint: The API endpoint path.
        json_data: Optional JSON body data.

    Returns:
        The parsed JSON response.
    """
    return post_request(
        url=get_fastq_unarchiving_url(endpoint),
        json_data=json_data
    )

# Create imports
from .create_helpers import create_job

# Query helpers
from .query_helpers import (
    get_job_from_job_id,
    get_unarchiving_job_list,
    get_job_list_for_fastq,
)

# Update helpers
from .update_helpers import (
    update_status
)

__all__ = [
    # Create helpers
    "create_job",

    # Query helpers
    "get_job_from_job_id",
    "get_unarchiving_job_list",
    "get_job_list_for_fastq",

    # Update helpers
    "update_status"
]