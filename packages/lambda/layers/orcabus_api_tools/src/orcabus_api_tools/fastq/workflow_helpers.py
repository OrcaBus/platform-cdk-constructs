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
