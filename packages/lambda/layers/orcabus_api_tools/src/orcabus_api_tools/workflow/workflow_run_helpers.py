#!/usr/bin/env python3

"""
Helpers for using the workflow run API endpoint
"""
from copy import copy

# Standard imports
from requests import HTTPError
from . import get_workflow_request_response_results, get_workflow_request

# Local imports
from .globals import WORKFLOW_RUN_ENDPOINT
from .models import WorkflowRun, State


def get_workflow_run(workflow_run_orcabus_id: str) -> WorkflowRun:
    """
    Get the workflow run from the workflow run id
    :param workflow_run_orcabus_id:
    :return:
    """
    # Get workflow run
    try:
        workflow_run = get_workflow_request(f"{WORKFLOW_RUN_ENDPOINT}/{workflow_run_orcabus_id}")
    except HTTPError as e:
        from .errors import WorkflowRunNotFoundError
        raise WorkflowRunNotFoundError(workflow_run_id=workflow_run_orcabus_id) from e

    # Get the workflow attribute of the workflow_run, make sure it uses 'name' and 'version'
    # Rather than 'workflowName' and 'workflowVersion'
    workflow_obj = copy(workflow_run.get("workflow", {}))
    if 'workflowName' in workflow_obj:
        workflow_obj['name'] = workflow_obj.pop('workflowName')
    if 'workflowVersion' in workflow_obj:
        workflow_obj['version'] = workflow_obj.pop('workflowVersion')

    # Re-add the workflow object to the workflow_run
    workflow_run['workflow'] = workflow_obj

    return workflow_run


def get_workflow_run_from_portal_run_id(portal_run_id: str) -> WorkflowRun:
    """
    Get workflow run from the portal run id
    :param portal_run_id:
    :return:
    """
    from .errors import WorkflowRunNotFoundError

    # We have an internal id, convert to int
    params = {
        "portalRunId": portal_run_id
    }

    workflow_runs_list = get_workflow_request_response_results(WORKFLOW_RUN_ENDPOINT, params)

    if len(workflow_runs_list) == 0:
        raise WorkflowRunNotFoundError(portal_run_id=portal_run_id)

    try:
        return get_workflow_run(
            workflow_runs_list[0]['orcabusId'],
        )
    except HTTPError as e:
        raise WorkflowRunNotFoundError(portal_run_id=portal_run_id) from e


def get_workflow_run_state_from_state_orcabus_id(
    workflow_run_orcabus_id: str, state_orcabus_id: str
)  -> State:

    # Get workflow run state
    try:
        return next(
            filter(
                lambda workflow_state_iter_: workflow_state_iter_["orcabusId"] == state_orcabus_id,
                get_workflow_request(f"{WORKFLOW_RUN_ENDPOINT}/{workflow_run_orcabus_id}/state")
            )
        )
    except HTTPError as e:
        from .errors import WorkflowRunStateNotFoundError
        raise WorkflowRunStateNotFoundError(
            workflow_run_id=workflow_run_orcabus_id,
            status=state_orcabus_id
        ) from e


def get_workflow_run_state(workflow_run_orcabus_id: str, status: str) -> State:
    """
    Get workflow run state from the workflow run orcabus id
    :param workflow_run_orcabus_id:
    :param status:
    :return:
    """
    # Get workflow run state
    try:
        return next(
            filter(
                lambda workflow_state_iter_: workflow_state_iter_["status"] == status,
                get_workflow_request(f"{WORKFLOW_RUN_ENDPOINT}/{workflow_run_orcabus_id}/state")
            )
        )
    except HTTPError as e:
        from .errors import WorkflowRunStateNotFoundError
        raise WorkflowRunStateNotFoundError(
            workflow_run_id=workflow_run_orcabus_id,
            status=status
        ) from e
