#!/usr/bin/env python3

"""
Validate NTSM
"""
from orcabus_api_tools.fastq import get_fastq_request
from orcabus_api_tools.fastq.globals import FASTQ_SET_ENDPOINT


def validate_ntsm_internal(fastq_set_id: str) -> bool:
    """
    Hit the fastq set endpoint with :validateNtsmInternal
    """
    return get_fastq_request(
        f"{FASTQ_SET_ENDPOINT}/{fastq_set_id}:validateNtsmInternal"
    )['related']


def validate_ntsm_external(fastq_set_id: str, external_fastq_set_id: str) -> bool:
    """
    Hit the fastq set endpoint with :validateNtsmExternal
    """
    return get_fastq_request(
        f"{FASTQ_SET_ENDPOINT}/{fastq_set_id}:validateNtsmExternal/{external_fastq_set_id}"
    )['related']
