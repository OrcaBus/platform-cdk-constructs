#!/usr/bin/env python3

"""
Workflow helpers - a collection of helper functions for the workflow

- to_cwl: Given a fastq id, convert to a cwl file
"""

# Standard library imports
from typing import List, Optional

# Local imports
from . import get_fastq_request
from .globals import FASTQ_ENDPOINT, FASTQ_SET_ENDPOINT
from .models import FastqListRowDict


def to_fastq_list_row(
        fastq_id: str,
        bucket: Optional[str] = None,
        key_prefix: Optional[str] = None,
) -> FastqListRowDict:
    """Convert a FASTQ record to a workflow-compatible FastqListRow dictionary.

    Args:
        fastq_id: The FASTQ identifier to convert.
        bucket: Optional S3 bucket override for the file URIs.
        key_prefix: Optional S3 key prefix override for the file URIs.

    Returns:
        A FastqListRowDict suitable for use in CWL/WDL workflow inputs.
    """
    return get_fastq_request(
        f"{FASTQ_ENDPOINT}/{fastq_id}/toFastqListRow",
        params=dict(filter(
            lambda param_iter_: param_iter_[1] is not None,
            {
                "bucket": bucket,
                "keyPrefix": key_prefix,
            }.items()
        ))
    )


def to_fastq_list_rows(
        fastq_set_id: str,
        bucket: Optional[str] = None,
        key_prefix: Optional[str] = None,
) -> List[FastqListRowDict]:
    """Convert all FASTQs in a FASTQ set to workflow-compatible FastqListRow dictionaries.

    Args:
        fastq_set_id: The FASTQ set identifier.
        bucket: Optional S3 bucket override for the file URIs.
        key_prefix: Optional S3 key prefix override for the file URIs.

    Returns:
        A list of FastqListRowDict objects suitable for use in CWL/WDL workflow inputs.
    """
    return get_fastq_request(
        f"{FASTQ_SET_ENDPOINT}/{fastq_set_id}/toFastqListRows",
        params=dict(filter(
            lambda param_iter_: param_iter_[1] is not None,
            {
                "bucket": bucket,
                "keyPrefix": key_prefix,
            }.items()
        ))
    )
