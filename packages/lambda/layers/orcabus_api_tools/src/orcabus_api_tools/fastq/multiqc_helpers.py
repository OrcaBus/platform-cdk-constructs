#!/usr/bin/env python3

"""
Run MultiQC on a list of fastq ids
"""

# Standard imports
from typing import List, Optional

# Custom imports
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


def update_multiqc_job_status(
        job_id: str,
        status: str,
        steps_execution_arn: Optional[str] = None,
        output_uri: Optional[str] = None
):
    return fastq_patch_request(
        f"{MULTIQC_ENDPOINT}/{job_id}",
        json_data=dict(filter(
            lambda kv_iter_: kv_iter_[1] is not None,
            {
                "status": status,
                "stepsExecutionArn": steps_execution_arn,
                "multiqcOutputHtmlUri": output_uri
            }.items())
        )
    )
