#!/usr/bin/env python3

"""
Getting the payload helpers
"""

# Standard imports
from typing import Dict

from . import get_workflow_request
# Local imports
from .globals import PAYLOAD_ENDPOINT
from .models import Payload


def get_payload(payload_id: str) -> Dict:
    """
    Get payload from the payload id
    :param payload_id:
    :return:
    """
    # Get subject
    return get_workflow_request(f"{PAYLOAD_ENDPOINT}/{payload_id}")


def get_payload_from_state_orcabus_id(workflow_run_orcabus_id: str, state_orcabus_id: str):
    """
    Given the workflow_run_orcabus_id and status, get the payload for that status
    :param workflow_run_orcabus_id:
    :param state_orcabus_id:
    :return:
    """
    from .workflow_run_helpers import get_workflow_run_state_from_state_orcabus_id

    # Get the workflow run state
    workflow_run_state_payload_id = get_workflow_run_state_from_state_orcabus_id(workflow_run_orcabus_id, state_orcabus_id)['payload']

    # Get the payload
    return get_payload(workflow_run_state_payload_id)


def get_latest_payload_from_workflow_run(workflow_run_orcabus_id: str) -> Payload:
    """
    Get the payload from the workflow run
    :param workflow_run_orcabus_id:
    :return:
    """
    from .workflow_run_helpers import get_workflow_run

    # Get the workflow run
    workflow_run = get_workflow_run(workflow_run_orcabus_id)

    # Get the payload
    return Payload(**get_payload_from_state_orcabus_id(
        workflow_run_orcabus_id=workflow_run_orcabus_id,
        state_orcabus_id=workflow_run['currentState']['orcabusId']
    ))


def get_latest_payload_from_portal_run_id(portal_run_id: str) -> Payload:
    from .workflow_run_helpers import get_workflow_run_from_portal_run_id

    # Get the workflow run
    workflow_run = get_workflow_run_from_portal_run_id(portal_run_id)

    # Get the payload
    return Payload(**get_payload_from_state_orcabus_id(
        workflow_run_orcabus_id=workflow_run['orcabusId'],
        state_orcabus_id=workflow_run['currentState']['orcabusId']
    ))
