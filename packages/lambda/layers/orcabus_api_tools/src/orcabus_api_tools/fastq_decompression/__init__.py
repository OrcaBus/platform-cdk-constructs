#!/usr/bin/env python3

"""Fastq decompression service toolkit for managing ORA-to-GZIP decompression jobs."""

# Standard imports
from typing import Dict, Optional

# Local imports
from .globals import FASTQ_DECOMPRESSION_SUBDOMAIN_NAME
from ..utils.requests_helpers import (
    get_request_response_results, get_url, patch_request, get_request, post_request
)


# Get url for the subdomain
def get_fastq_decompression_url(endpoint: str) -> str:
    """Get the full URL for the fastq decompression service endpoint.

    Args:
        endpoint: The API endpoint path.

    Returns:
        The full URL for the fastq decompression service.
    """
    return get_url(
        endpoint=endpoint,
        subdomain=FASTQ_DECOMPRESSION_SUBDOMAIN_NAME,
    )


# Wrappers
def get_fastq_decompression_request(
        endpoint: str,
        params: Optional[Dict] = None,
):
    """Execute an authenticated GET request to the fastq decompression service.

    Args:
        endpoint: The API endpoint path.
        params: Optional query parameters.

    Returns:
        The parsed JSON response.
    """
    return get_request(
        url=get_fastq_decompression_url(endpoint),
        params=params
    )


def get_fastq_decompression_request_response_results(
        endpoint: str,
        params: Optional[Dict] = None,
):
    """Execute a paginated GET request to the fastq decompression service.

    Args:
        endpoint: The API endpoint path.
        params: Optional query parameters.

    Returns:
        A list of all results across all pages.
    """
    return get_request_response_results(
        url=get_fastq_decompression_url(endpoint),
        params=params
    )


def fastq_decompression_patch_request(
    endpoint: str,
    json_data: Optional[Dict] = None,
):
    """Execute an authenticated PATCH request to the fastq decompression service.

    Args:
        endpoint: The API endpoint path.
        json_data: Optional JSON body data.

    Returns:
        The parsed JSON response.
    """
    return patch_request(
        url=get_fastq_decompression_url(endpoint),
        json_data=json_data
    )


def fastq_decompression_post_request(
    endpoint: str,
    json_data: Optional[Dict] = None,
):
    """Execute an authenticated POST request to the fastq decompression service.

    Args:
        endpoint: The API endpoint path.
        json_data: Optional JSON body data.

    Returns:
        The parsed JSON response.
    """
    return post_request(
        url=get_fastq_decompression_url(endpoint),
        json_data=json_data
    )

# Create imports
from .create_helpers import create_job

# Query helpers
from .query_helpers import (
    get_job_from_job_id,
    get_decompression_job_list,
    get_job_list_for_fastq
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
    "get_decompression_job_list",
    "get_job_list_for_fastq",

    # Update helpers
    "update_status",
]
