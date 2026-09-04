#!/usr/bin/env python3

"""
Interact with the case service
"""

# Standard imports
from typing import Dict, List, Optional, cast

# Local imports
from . import (
    get_case_request,
    get_case_request_response_results,
    case_post_request,
)
from .globals import CASE_ENDPOINT
from .models import Case


def list_cases(params: Optional[Dict] = None) -> List[Case]:
    """
    List all cases.

    Uses the ``/api/v1/case/`` endpoint.

    :param params: Optional query parameters to filter the returned cases.
    :return: A list of case objects.
    """
    return cast(
        List[Case],
        get_case_request_response_results(
            endpoint=f"{CASE_ENDPOINT}/",
            params=params,
        )
    )


def get_case(orcabus_id: str) -> Case:
    """
    Get a single case by its orcabus id.

    Uses the ``/api/v1/case/{orcabusId}`` endpoint.

    :param orcabus_id: The orcabus id of the case to retrieve.
    :return: The case object.
    """
    return cast(
        Case,
        get_case_request(
            endpoint=f"{CASE_ENDPOINT}/{orcabus_id}",
        )
    )


def link_entity_to_case(
        orcabus_id: str,
        entity_type: str,
        entity_id: str,
) -> Dict:
    """
    Link an external entity to a case.

    Uses the ``/api/v1/case/{orcabusId}/external-entity/`` endpoint.

    :param orcabus_id: The orcabus id of the case to link the entity to.
    :param entity_type: The type of the external entity being linked.
    :param entity_id: The identifier of the external entity being linked.
    :return: The API response containing the linked entity details.
    """
    return case_post_request(
        endpoint=f"{CASE_ENDPOINT}/{orcabus_id}/external-entity/",
        json_data={
            "entityType": entity_type,
            "entityId": entity_id,
        },
    )


def sync_case_from_redcap(
        orcabus_id: str,
        json_data: Optional[Dict] = None,
) -> Dict:
    """
    Sync a case from RedCap.

    Uses the ``/api/v1/case/{orcabusId}/sync-from-redcap/`` endpoint.

    :param orcabus_id: The orcabus id of the case to sync from RedCap.
    :param json_data: Optional JSON body with sync options.
    :return: The API response containing the sync result.
    """
    return case_post_request(
        endpoint=f"{CASE_ENDPOINT}/{orcabus_id}/sync-from-redcap/",
        json_data=json_data,
    )
