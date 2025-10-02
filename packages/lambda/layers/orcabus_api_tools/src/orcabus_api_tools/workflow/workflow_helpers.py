#!/usr/bin/env python3

"""
Get the workflow object
"""
from typing import Optional, List, cast

from . import get_workflow_request_response_results
from .globals import WORKFLOW_ENDPOINT
from .models import Workflow, ExecutionEngineType, ValidationStateType


def _convert_workflow(workflow_dict: dict) -> Workflow:
    """
    Convert a workflow dictionary to a Workflow object
    :param workflow_dict:
    :return:
    """
    workflow_dict = workflow_dict.copy()
    if "workflowName" in workflow_dict:
        workflow_dict["name"] = workflow_dict.pop("workflowName")
    if "workflowVersion" in workflow_dict:
        workflow_dict["version"] = workflow_dict.pop("workflowVersion")

    return cast(Workflow, workflow_dict)


def list_workflows(
        workflow_name: str,
        workflow_version: Optional[str] = None,
        code_version: Optional[str] = None,
        execution_engine: Optional[ExecutionEngineType] = None,
        execution_engine_pipeline_id: Optional[str] = None,
        validation_state: Optional[ValidationStateType] = None,
) -> List[Workflow]:
    """
    Given a workflow, list the workflow object
    :param workflow_name:
    :param workflow_version:
    :return:
    """

    # List all workflows
    workflows_list = get_workflow_request_response_results(
        WORKFLOW_ENDPOINT,
    )

    # For each workflow, check if workflowName / name or workflowVersion / version matches
    workflows_list = list(filter(
        lambda workflow_iter: workflow_iter.get("workflowName", workflow_iter.get("name")) == workflow_name,
        workflows_list
    ))

    if workflow_version:
        workflows_list = list(filter(
            lambda workflow_iter: workflow_iter.get("workflowVersion", workflow_iter.get("version")) == workflow_version,
            workflows_list
        ))

    if code_version:
        workflows_list = list(filter(
            lambda workflow_iter: workflow_iter.get("codeVersion", None) == code_version,
            workflows_list
        ))

    if execution_engine:
        workflows_list = list(filter(
            lambda workflow_iter: workflow_iter.get("executionEngine", None) == execution_engine,
            workflows_list
        ))

        # Might as well nest this, need to filter by execution engine first
        if execution_engine_pipeline_id:
            workflows_list = list(filter(
                lambda workflow_iter: workflow_iter.get("executionEnginePipelineId", None) == execution_engine_pipeline_id,
                workflows_list
            ))

    if validation_state:
        workflows_list = list(filter(
            lambda workflow_iter: workflow_iter.get("validationState", None) == validation_state,
            workflows_list
        ))

    # Convert to Workflow objects
    # This means converting workflowName to name and workflowVersion to version
    workflows_list: List[Workflow] = list(map(
        lambda workflow_iter: _convert_workflow(workflow_iter),
        workflows_list
    ))

    return workflows_list
