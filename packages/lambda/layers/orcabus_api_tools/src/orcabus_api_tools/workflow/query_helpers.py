#!/usr/bin/env python

"""
Get workflows from library id
"""

# Standard imports
from typing import List

# Local imports
from . import get_workflow_request_response_results
from .globals import WORKFLOW_RUN_ENDPOINT
from .models import WorkflowRunDetail


def get_workflows_from_analysis_run_id(analysis_run_id: str) -> List[WorkflowRunDetail]:
    """
    Use the query analysisRuns__analysisRunId to get workflows from an analysis run id
    :param analysis_run_id:
    :return:
    """
    return get_workflow_request_response_results(
        WORKFLOW_RUN_ENDPOINT,
        params={
            "analysisRun__orcabusId": analysis_run_id
        }
    )


def get_workflow_by_workflow_name(
        workflow_name: str,
) -> List[WorkflowRunDetail]:
    """
    Use the query name to get workflows from a workflow name
    :param workflow_name:
    :return:
    """

    return get_workflow_request_response_results(
        WORKFLOW_RUN_ENDPOINT,
        params={
            "workflow__name": workflow_name
        }
    )
