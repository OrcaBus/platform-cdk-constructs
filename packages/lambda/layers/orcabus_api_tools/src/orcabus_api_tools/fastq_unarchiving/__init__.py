#!/usr/bin/env python3

# Standard imports
from typing import Dict, Optional

# Local imports
from .globals import FASTQ_UNARCHIVING_SUBDOMAIN_NAME
from ..utils.requests_helpers import (
    get_request_response_results, get_url, patch_request, get_request
)


# Get url for the subdomain
def get_fastq_unarchiving_url(endpoint: str) -> str:
    """
    Get the URL for the Metadata endpoint
    :param endpoint:
    :return:
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
    return get_request(
        url=get_fastq_unarchiving_url(endpoint),
        params=params
    )


def get_fastq_unarchiving_request_response_results(
        endpoint: str,
        params: Optional[Dict] = None,
):
    return get_request_response_results(
        url=get_fastq_unarchiving_url(endpoint),
        params=params
    )


def fastq_unarchiving_patch_request(
    endpoint: str,
    params: Optional[Dict] = None,
):
    return patch_request(
        url=get_fastq_unarchiving_url(endpoint),
        params=params
    )


def fastq_unarchiving_post_request(
    endpoint: str,
    params: Optional[Dict] = None,
):
    return patch_request(
        url=get_fastq_unarchiving_url(endpoint),
        params=params
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