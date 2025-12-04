#!/usr/bin/env python3

"""
Get the workflow object
"""
from typing import Optional, List, cast

from . import get_workflow_request_response_results
from .globals import WORKFLOW_ENDPOINT
from .models import Workflow, ExecutionEngineType, ValidationStateType


def list_workflows(
        workflow_name: str,
        workflow_version: Optional[str] = None,
        code_version: Optional[str] = None,
        execution_engine: Optional[ExecutionEngineType] = None,
        execution_engine_pipeline_id: Optional[str] = None,
        validation_state: Optional[ValidationStateType] = None,
) -> List[Workflow]:
    """
    List workflow objects matching the provided filters.
    :param workflow_name: The name of the workflow to filter by.
    :param workflow_version: (Optional) The version of the workflow to filter by.
    :param code_version: (Optional) The code version to filter by.
    :param execution_engine: (Optional) The execution engine type to filter by.
    :param execution_engine_pipeline_id: (Optional) The execution engine pipeline ID to filter by. Only used if execution_engine is specified.
    :param validation_state: (Optional) The validation state to filter by.
    :return: A list of Workflow objects matching the provided filters.
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

    return workflows_list
