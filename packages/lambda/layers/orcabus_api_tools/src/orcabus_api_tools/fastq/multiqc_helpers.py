#!/usr/bin/env python3

"""
Run MultiQC on a list of fastq ids
"""
from typing import List

from orcabus_api_tools.fastq import fastq_patch_request
from orcabus_api_tools.fastq.globals import MULTIQC_ENDPOINT


def run_multiqc(fastq_id_list: List[str]) -> str:
    """
    Run multiqc on a list of fastq ids
    Return the presigned url to the output multiqc report
    :param fastq_id_list: List of fastq ids to run multiqc on
    """
    return fastq_patch_request(
        f"{MULTIQC_ENDPOINT}",
        json_data=fastq_id_list
    )
