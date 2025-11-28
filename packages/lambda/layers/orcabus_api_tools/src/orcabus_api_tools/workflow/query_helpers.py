#!/usr/bin/env python

"""
Get workflows from library id
"""
# Standard imports
import warnings
from typing import List, Optional

# Local imports
from . import get_workflow_request_response_results
from .globals import WORKFLOW_RUN_ENDPOINT
from .models import WorkflowRunDetail


def list_workflow_runs(
        workflow_name: Optional[str] = None,
        workflow_version: Optional[str] = None,
        code_version: Optional[str] = None,
        current_status: Optional[str] = None,
        analysis_run_id: Optional[str] = None,
) -> List[WorkflowRunDetail]:
    """
    Use the query name to get workflows
    :param workflow_name:
    :param workflow_version:
    :param code_version:
    :param current_status:
    :return:
    """
    return get_workflow_request_response_results(
        WORKFLOW_RUN_ENDPOINT,
        params=dict(filter(
            lambda item: item[1] is not None,
            {
                "workflow__name": workflow_name,
                "workflow__version": workflow_version,
                "workflow__codeVersion": code_version,
                "currentState__status": current_status,
                "analysisRun__orcabusId": analysis_run_id
            }.items()
        ))
    )


# Deprecated
def list_workflow_runs_by_workflow_name(
        workflow_name: str,
) -> List[WorkflowRunDetail]:
    """
    Use the query name to get workflows from a workflow name
    :param workflow_name:
    :return:
    """
    warnings.warn(DeprecationWarning(
        "This function is deprecated, "
        "please use list_workflow_runs instead"
    ))
    return get_workflow_request_response_results(
        WORKFLOW_RUN_ENDPOINT,
        params=dict(filter(
            lambda item: item[1] is not None,
            {
                "workflow__name": workflow_name,
            }.items()
        ))
    )


def get_workflow_by_workflow_name(workflow_name: str) -> List[WorkflowRunDetail]:
    warnings.warn(DeprecationWarning(
        "This function is deprecated, "
        "please use list_workflow_runs(workflow_name=workflow_name) instead"
    ))
    return list_workflow_runs(workflow_name=workflow_name)


def get_workflows_from_analysis_run_id(analysis_run_id: str) -> List[WorkflowRunDetail]:
    warnings.warn(DeprecationWarning(
        "This function is deprecated, "
        "please use list_workflow_runs(analysis_run_id=analysis_run_id) instead"
    ))
    return list_workflow_runs(analysis_run_id=analysis_run_id)


def list_workflow_runs_from_analysis_run_id(analysis_run_id: str) -> List[WorkflowRunDetail]:
    """
    Use the query analysisRuns__analysisRunId to get workflows from an analysis run id
    :param analysis_run_id:
    :return:
    """
    warnings.warn(DeprecationWarning(
        "This function is deprecated, "
        "please use list_workflow_runs(analysis_run_id=analysis_run_id) instead"
    ))
    return list_workflow_runs(
        analysis_run_id=analysis_run_id
    )
