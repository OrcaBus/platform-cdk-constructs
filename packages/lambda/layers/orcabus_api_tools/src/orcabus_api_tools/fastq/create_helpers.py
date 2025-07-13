#!/usr/bin/env python3

"""
Update helpers for the update script.

- add_qc_stats
- add_read_count
- add_ntsm_storage_object / add_ntsm
- add_fastq_pair_storage_object / add_read_set
- detach_fastq_pair_storage_object / detach_read_set
- validate
- invalidate
"""

# Standard imports
from typing import Unpack

# Local imports
from . import fastq_post_request
from .globals import FASTQ_ENDPOINT, FASTQ_SET_ENDPOINT
from .models import Fastq, FastqSet, FastqCreate, FastqSetCreate


def create_fastq_list_row_object(**kwargs: Unpack[FastqCreate]) -> Fastq:
    """
    DEPRECATED: Use create_fastq_object instead.
    """
    return create_fastq_object(**kwargs)


def create_fastq_object(**kwargs: Unpack[FastqCreate]) -> Fastq:
    """
    Add a fastq list row object to the database.
    Returns the created fastq list row object
    """
    # Raise error if any of the kwargs are not in the FastqCreate
    for key in kwargs.keys():
        if key not in FastqCreate.__annotations__:
            raise ValueError(f"Invalid parameter: {key}")

    return Fastq(
        **fastq_post_request(
            endpoint=FASTQ_ENDPOINT,
            json_data=dict(kwargs)
        )
    )


def create_fastq_set_object(**kwargs: Unpack[FastqSetCreate]) -> FastqSet:
    """
    Add a fastq set object to the database.
    Returns the created fastq set object
    """
    # Raise error if any of the kwargs are not in the FastqCreate
    for key in kwargs.keys():
        if key not in FastqSetCreate.__annotations__:
            raise ValueError(f"Invalid parameter: {key}")

    return FastqSet(
        **fastq_post_request(
            endpoint=FASTQ_SET_ENDPOINT,
            json_data=dict(kwargs)
        )
    )
