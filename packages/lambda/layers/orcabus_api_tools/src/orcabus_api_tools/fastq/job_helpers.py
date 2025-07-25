#!/usr/bin/env python3

"""
Update helpers for the update script.

- run_qc_stats
- run_ntsm
- run_file_compression_information
"""
# Standard imports

# Local imports
from . import fastq_patch_request
from .globals import FASTQ_ENDPOINT
from .models import Job


def run_qc_stats(fastq_id: str) -> Job:
    """
    Add QC stats to a fastq_id.

    :param fastq_id: Fastq str
    """
    return Job(
        **fastq_patch_request(
            f"{FASTQ_ENDPOINT}/{fastq_id}:runQcStats"
        )
    )


def run_ntsm(fastq_id: str) -> Job:
    """
    Run ntsm for a fastq_id.

    :param fastq_id: Fastq str
    """
    return Job(
        **fastq_patch_request(
            f"{FASTQ_ENDPOINT}/{fastq_id}:runNtsm"
        )
    )

def run_file_compression_stats(fastq_id: str) -> Job:
    """
    Run file compression stats for a fastq_id.

    :param fastq_id: Fastq str
    """
    return Job(
        **fastq_patch_request(
            f"{FASTQ_ENDPOINT}/{fastq_id}:runFileCompressionInformation"
        )
    )

def run_read_count_stats(fastq_id: str) -> Job:
    """
    Run file compression stats for a fastq_id.

    :param fastq_id: Fastq str
    """
    return Job(
        **fastq_patch_request(
            f"{FASTQ_ENDPOINT}/{fastq_id}:runReadCountInformation"
        )
    )
