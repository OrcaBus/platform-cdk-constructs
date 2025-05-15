#!/usr/bin/env python3

"""
Workflow helpers - a collection of helper functions for the workflow

- to_cwl: Given a fastq id, convert to a cwl file
"""

# Standard library imports
from typing import List
# Local imports
from . import get_fastq_request
from .globals import FASTQ_LIST_ROW_ENDPOINT, FASTQ_SET_ENDPOINT
from .models import FastqListRowDict


def to_fastq_list_row(fastq_id) -> FastqListRowDict:
    return get_fastq_request(
        f"{FASTQ_LIST_ROW_ENDPOINT}/{fastq_id}/toFastqListRow"
    )

def to_fastq_list_rows(fastq_set_id: str) -> List[FastqListRowDict]:
    return get_fastq_request(
        f"{FASTQ_SET_ENDPOINT}/{fastq_set_id}/toFastqListRows"
    )
