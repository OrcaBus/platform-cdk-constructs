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
        html_output_uri: Optional[str] = None,
        parquet_output_uri: Optional[str] = None
):
    """
    Update the status of a MultiQC job.

    :param job_id: The unique identifier of the MultiQC job.
    :param status: The new status of the job (e.g., "running", "completed", "failed").
    :param steps_execution_arn: (Optional) The ARN of the step function execution associated with the job.
    :param html_output_uri: (Optional) The URI of the output MultiQC report.
    :param parquet_output_uri: (Optional) The URI of the output MultiQC parquet file.
    :return: The response from the fastq_patch_request function.
    """
    return fastq_patch_request(
        f"{MULTIQC_ENDPOINT}/{job_id}",
        json_data=dict(filter(
            lambda kv_iter_: kv_iter_[1] is not None,
            {
                "status": status,
                "stepsExecutionArn": steps_execution_arn,
                "multiqcHtml": {
                    "s3Uri": html_output_uri
                },
                "multiqcParquet": {
                    "s3Uri": parquet_output_uri
                }
            }.items())
        )
    )
