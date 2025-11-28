#!/usr/bin/env python3

"""
Getting the payload helpers
"""

# Standard imports
from typing import Optional, cast

# Local imports
from . import get_workflow_request
from .globals import PAYLOAD_ENDPOINT
from .models import Payload


def get_payload(payload_id: str) -> Optional[Payload]:
    """
    Get payload from the payload id
    :param payload_id:
    :return:
    """
    # Get payload
    return cast(Payload, get_workflow_request(f"{PAYLOAD_ENDPOINT}/{payload_id}"))


def get_payload_from_state_orcabus_id(workflow_run_orcabus_id: str, state_orcabus_id: str) -> Optional[Payload]:
    """
    Given the workflow_run_orcabus_id and status, get the payload for that status
    :param workflow_run_orcabus_id:
    :param state_orcabus_id:
    :return:
    """
    from .workflow_run_helpers import get_workflow_run_state_from_state_orcabus_id

    # Get the workflow run state
    workflow_run_state_payload_id = get_workflow_run_state_from_state_orcabus_id(workflow_run_orcabus_id, state_orcabus_id)['payload']

    if workflow_run_state_payload_id is None:
        return None

    # Get the payload
    return get_payload(workflow_run_state_payload_id)


def get_latest_payload_from_workflow_run(workflow_run_orcabus_id: str) -> Optional[Payload]:
    """
    Get the payload from the workflow run
    :param workflow_run_orcabus_id:
    :return:
    """
    from .workflow_run_helpers import get_workflow_run

    # Get the workflow run
    workflow_run = get_workflow_run(workflow_run_orcabus_id)

    # Get the payload from the current state
    return get_payload_from_state_orcabus_id(
        workflow_run_orcabus_id=workflow_run_orcabus_id,
        state_orcabus_id=workflow_run['currentState']['orcabusId']
    )


def get_latest_payload_from_portal_run_id(portal_run_id: str) -> Payload:
    from .workflow_run_helpers import get_workflow_run_from_portal_run_id

    # Get the workflow run
    workflow_run = get_workflow_run_from_portal_run_id(portal_run_id)

    # Get the payload
    return Payload(**get_payload_from_state_orcabus_id(
        workflow_run_orcabus_id=workflow_run['orcabusId'],
        state_orcabus_id=workflow_run['currentState']['orcabusId']
    ))
