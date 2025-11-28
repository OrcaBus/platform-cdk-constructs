#!/usr/bin/env python3

"""
Update helpers for the update script.

- run_qc_stats
- run_ntsm
- run_file_compression_information
"""
from typing import Dict, Any

# Standard imports

# Local imports
from . import fastq_patch_request
from .globals import FASTQ_ENDPOINT, FASTQ_SET_ENDPOINT
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

def run_extract_fingerprint(
        fastq_set_id: str,
        reference_name: str,
        bam_uri: str
) -> Dict[str, Any]:
    """
    Run extract fingerprint for a fastq_set_id.

    :param bam_uri:
    :param reference_name:
    :param fastq_set_id: Fastq set id
    """
    return fastq_patch_request(
        f"{FASTQ_SET_ENDPOINT}/{fastq_set_id}:runExtractFingerprint",
        params={
            "referenceName": reference_name
        },
        json_data={
            "s3Uri": bam_uri
        }
    )
