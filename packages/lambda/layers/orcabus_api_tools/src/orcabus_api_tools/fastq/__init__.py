#!/usr/bin/env python3

# Standard imports
from typing import Dict, Optional

# Local imports
from .globals import FASTQ_SUBDOMAIN_NAME
from ..utils.requests_helpers import (
    get_request_response_results, get_url, patch_request, get_request, post_request
)


# Get url for the subdomain
def get_fastq_url(endpoint: str) -> str:
    """
    Get the URL for the Metadata endpoint
    :param endpoint:
    :return:
    """
    return get_url(
        endpoint=endpoint,
        subdomain=FASTQ_SUBDOMAIN_NAME,
    )


# Wrappers
def get_fastq_request(
        endpoint: str,
        params: Optional[Dict] = None,
):
    return get_request(
        url=get_fastq_url(endpoint),
        params=params
    )


def get_fastq_request_response_results(
        endpoint: str,
        params: Optional[Dict] = None,
):
    return get_request_response_results(
        url=get_fastq_url(endpoint),
        params=params
    )


def fastq_patch_request(
    endpoint: str,
    params: Optional[Dict] = None,
):
    return patch_request(
        url=get_fastq_url(endpoint),
        params=params
    )


def fastq_post_request(
    endpoint: str,
    params: Optional[Dict] = None,
):
    return post_request(
        url=get_fastq_url(endpoint),
        params=params
    )



# Expose the functions

# Create
from .create_helpers import (
    create_fastq_set_object,
    create_fastq_list_row_object
)

# Job
from .job_helpers import (
    run_qc_stats,
    run_ntsm,
    run_file_compression_stats
)

# Query
from .query_helpers import (
    get_fastq,
    get_fastq_set,
    get_fastqs,
    get_fastq_sets,
    get_fastqs_in_instrument_run_id,
    get_fastqs_in_library,
    get_fastqs_batched,
    get_fastqs_in_library_list,
    get_fastqs_in_libraries_and_instrument_run_id,
    get_fastqs_in_sample,
    get_fastqs_in_sample_list,
    get_fastqs_in_subject,
    get_fastqs_in_individual,
    get_fastqs_in_project,
    get_fastq_list_rows_in_fastq_set,
    get_fastq_jobs,
)

# Updaters
from .update_helpers import (
    add_qc_stats,
    add_read_count,
    add_file_compression_information,
    add_ntsm_storage_object,
    add_read_set,
    detach_read_set,
    validate_fastq,
    invalidate_fastq,
    link_fastq_list_row_to_fastq_set,
    unlink_fastq_list_row_from_fastq_set,
    allow_additional_fastqs_to_fastq_set,
    disallow_additional_fastqs_to_fastq_set,
    set_is_current_fastq_set,
    set_is_not_current_fastq_set,
)

# Workflow
from .workflow_helpers import (
    to_fastq_list_row,
    to_fastq_list_rows
)


__all__ = [
    # Create
    "create_fastq_set_object",
    "create_fastq_list_row_object",
    # Job
    "run_qc_stats",
    "run_ntsm",
    "run_file_compression_stats",
    # Query
    "get_fastq",
    "get_fastq_set",
    "get_fastqs",
    "get_fastq_sets",
    "get_fastqs_in_instrument_run_id",
    "get_fastqs_in_library",
    "get_fastqs_batched",
    "get_fastqs_in_library_list",
    "get_fastqs_in_libraries_and_instrument_run_id",
    "get_fastqs_in_sample",
    "get_fastqs_in_sample_list",
    "get_fastqs_in_subject",
    "get_fastqs_in_individual",
    "get_fastqs_in_project",
    "get_fastq_list_rows_in_fastq_set",
    "get_fastq_jobs",
    # Updaters
    "add_qc_stats",
    "add_read_count",
    "add_file_compression_information",
    "add_ntsm_storage_object",
    "add_read_set",
    "detach_read_set",
    "validate_fastq",
    "invalidate_fastq",
    "link_fastq_list_row_to_fastq_set",
    "unlink_fastq_list_row_from_fastq_set",
    "allow_additional_fastqs_to_fastq_set",
    "disallow_additional_fastqs_to_fastq_set",
    "set_is_current_fastq_set",
    "set_is_not_current_fastq_set",
    # Workflow
    "to_fastq_list_row",
    "to_fastq_list_rows",
]

