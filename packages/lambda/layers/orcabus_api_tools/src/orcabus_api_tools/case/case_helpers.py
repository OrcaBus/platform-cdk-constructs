#!/usr/bin/env python3

"""
Interact with the case service.

Endpoints mirror the Case Manager API
(https://case.prod.umccr.org/schema/openapi.json).
"""

# Standard imports
from typing import Dict, List, Optional, cast

# Local imports
from . import (
    get_case_request,
    get_case_request_response_results,
    case_post_request,
    case_patch_request,
)
from .globals import (
    CASE_ENDPOINT,
    STATE_ENDPOINT,
    COMMENT_ENDPOINT,
    EXTERNAL_ENTITY_ENDPOINT,
    USER_ENDPOINT,
)
from .models import (
    CaseDetail,
    CaseExternalEntityLinkCreate,
    CaseTimeline,
    CaseUserCreate,
    Comment,
    ExternalEntityDetail,
    State,
    StateDetail,
    UserDetail,
)


# Case
def list_cases(params: Optional[Dict] = None) -> List[CaseDetail]:
    """
    List all cases.

    Uses the ``GET /api/v1/case/`` endpoint.

    :param params: Optional query parameters to filter the returned cases.
        Supported keys include ``isActive``, ``latestState``, ``libraryId``,
        ``ordering``, ``search``, ``page`` and ``rowsPerPage``.
    :return: A list of case objects.
    """
    return cast(
        List[CaseDetail],
        get_case_request_response_results(
            endpoint=f"{CASE_ENDPOINT}/",
            params=params,
        )
    )


def get_case(orcabus_id: str) -> CaseDetail:
    """
    Get a single case by its orcabus id.

    Uses the ``GET /api/v1/case/{orcabusId}/`` endpoint.

    :param orcabus_id: The orcabus id of the case to retrieve.
    :return: The case object.
    """
    return cast(
        CaseDetail,
        get_case_request(
            endpoint=f"{CASE_ENDPOINT}/{orcabus_id}/",
        )
    )


def update_case(
        orcabus_id: str,
        json_data: Dict,
) -> CaseDetail:
    """
    Partially update a case.

    Uses the ``PATCH /api/v1/case/{orcabusId}/`` endpoint. Only writable fields
    are accepted (see ``PatchedCaseDetailRequest``): ``alias``,
    ``rnasumReferences``, ``description``, ``studyType``, ``isReportRequired``,
    ``isNataAccredited``, ``links`` and ``dueDate``.

    :param orcabus_id: The orcabus id of the case to update.
    :param json_data: The writable fields to update.
    :return: The updated case object.
    """
    return cast(
        CaseDetail,
        case_patch_request(
            endpoint=f"{CASE_ENDPOINT}/{orcabus_id}/",
            json_data=json_data,
        )
    )


def get_case_activity(orcabus_id: str) -> List[CaseTimeline]:
    """
    Get the activity timeline for a case.

    Uses the ``GET /api/v1/case/{orcabusId}/activity/`` endpoint.

    :param orcabus_id: The orcabus id of the case.
    :return: A list of timeline entries.
    """
    return cast(
        List[CaseTimeline],
        get_case_request_response_results(
            endpoint=f"{CASE_ENDPOINT}/{orcabus_id}/activity/",
        )
    )


def list_case_states(orcabus_id: str) -> List[State]:
    """
    List the states for a case.

    Uses the ``GET /api/v1/case/{orcabusId}/states/`` endpoint.

    :param orcabus_id: The orcabus id of the case.
    :return: A list of state objects.
    """
    return cast(
        List[State],
        get_case_request_response_results(
            endpoint=f"{CASE_ENDPOINT}/{orcabus_id}/states/",
        )
    )


def link_entity_to_case(
        orcabus_id: str,
        external_entity_orcabus_id: str,
) -> CaseExternalEntityLinkCreate:
    """
    Link an external entity to a case.

    Uses the ``POST /api/v1/case/{orcabusId}/external-entity/`` endpoint.

    :param orcabus_id: The orcabus id of the case to link the entity to.
    :param external_entity_orcabus_id: The orcabus id of the external entity to link.
    :return: The API response containing the linked entity details.
    """
    return cast(
        CaseExternalEntityLinkCreate,
        case_post_request(
            endpoint=f"{CASE_ENDPOINT}/{orcabus_id}/external-entity/",
            json_data={
                "externalEntity": external_entity_orcabus_id,
            },
        )
    )


def add_user_to_case(
        orcabus_id: str,
        email: str,
        description: Optional[str] = None,
) -> CaseUserCreate:
    """
    Link a user (by email) to a case.

    Uses the ``POST /api/v1/case/{orcabusId}/user/`` endpoint.

    :param orcabus_id: The orcabus id of the case.
    :param email: The email of the user to link.
    :param description: Optional description for the link.
    :return: The API response containing the created link.
    """
    json_data: Dict = {"email": email}
    if description is not None:
        json_data["description"] = description
    return cast(
        CaseUserCreate,
        case_post_request(
            endpoint=f"{CASE_ENDPOINT}/{orcabus_id}/user/",
            json_data=json_data,
        )
    )


def sync_case_from_redcap(
        orcabus_id: str,
        json_data: Optional[Dict] = None,
) -> Dict:
    """
    Sync a case from RedCap.

    Uses the ``POST /api/v1/case/{orcabusId}/sync-from-redcap/`` endpoint.

    :param orcabus_id: The orcabus id of the case to sync from RedCap.
    :param json_data: Optional JSON body with sync options.
    :return: The API response containing the sync result.
    """
    return case_post_request(
        endpoint=f"{CASE_ENDPOINT}/{orcabus_id}/sync-from-redcap/",
        json_data=json_data,
    )


# State
def list_states(params: Optional[Dict] = None) -> List[StateDetail]:
    """
    List all states.

    Uses the ``GET /api/v1/state/`` endpoint.

    :param params: Optional query parameters to filter the returned states.
    :return: A list of state objects.
    """
    return cast(
        List[StateDetail],
        get_case_request_response_results(
            endpoint=f"{STATE_ENDPOINT}/",
            params=params,
        )
    )


def get_state(orcabus_id: str) -> StateDetail:
    """
    Get a single state by its orcabus id.

    Uses the ``GET /api/v1/state/{orcabusId}/`` endpoint.

    :param orcabus_id: The orcabus id of the state to retrieve.
    :return: The state object.
    """
    return cast(
        StateDetail,
        get_case_request(
            endpoint=f"{STATE_ENDPOINT}/{orcabus_id}/",
        )
    )


def create_state(json_data: Dict) -> StateDetail:
    """
    Create a state.

    Uses the ``POST /api/v1/state/`` endpoint. Requires ``status`` and ``case``
    (see ``StateDetailRequest``).

    :param json_data: The state fields.
    :return: The created state object.
    """
    return cast(
        StateDetail,
        case_post_request(
            endpoint=f"{STATE_ENDPOINT}/",
            json_data=json_data,
        )
    )


def archive_state(
        orcabus_id: str,
        json_data: Optional[Dict] = None,
) -> StateDetail:
    """
    Archive a state.

    Uses the ``PATCH /api/v1/state/{orcabusId}/archive/`` endpoint.

    :param orcabus_id: The orcabus id of the state to archive.
    :param json_data: Optional JSON body.
    :return: The archived state object.
    """
    return cast(
        StateDetail,
        case_patch_request(
            endpoint=f"{STATE_ENDPOINT}/{orcabus_id}/archive/",
            json_data=json_data,
        )
    )


# Comment
def list_comments(params: Optional[Dict] = None) -> List[Comment]:
    """
    List all comments.

    Uses the ``GET /api/v1/comment/`` endpoint.

    :param params: Optional query parameters to filter the returned comments.
    :return: A list of comment objects.
    """
    return cast(
        List[Comment],
        get_case_request_response_results(
            endpoint=f"{COMMENT_ENDPOINT}/",
            params=params,
        )
    )


def get_comment(orcabus_id: str) -> Comment:
    """
    Get a single comment by its orcabus id.

    Uses the ``GET /api/v1/comment/{orcabusId}/`` endpoint.

    :param orcabus_id: The orcabus id of the comment to retrieve.
    :return: The comment object.
    """
    return cast(
        Comment,
        get_case_request(
            endpoint=f"{COMMENT_ENDPOINT}/{orcabus_id}/",
        )
    )


def create_comment(json_data: Dict) -> Comment:
    """
    Create a comment.

    Uses the ``POST /api/v1/comment/`` endpoint (see ``CommentRequest``).

    :param json_data: The comment fields.
    :return: The created comment object.
    """
    return cast(
        Comment,
        case_post_request(
            endpoint=f"{COMMENT_ENDPOINT}/",
            json_data=json_data,
        )
    )


def archive_comment(
        orcabus_id: str,
        json_data: Optional[Dict] = None,
) -> Comment:
    """
    Archive a comment.

    Uses the ``PATCH /api/v1/comment/{orcabusId}/archive/`` endpoint.

    :param orcabus_id: The orcabus id of the comment to archive.
    :param json_data: Optional JSON body.
    :return: The archived comment object.
    """
    return cast(
        Comment,
        case_patch_request(
            endpoint=f"{COMMENT_ENDPOINT}/{orcabus_id}/archive/",
            json_data=json_data,
        )
    )


# External entity
def list_external_entities(params: Optional[Dict] = None) -> List[ExternalEntityDetail]:
    """
    List all external entities.

    Uses the ``GET /api/v1/external-entity/`` endpoint.

    :param params: Optional query parameters to filter the returned entities.
    :return: A list of external entity objects.
    """
    return cast(
        List[ExternalEntityDetail],
        get_case_request_response_results(
            endpoint=f"{EXTERNAL_ENTITY_ENDPOINT}/",
            params=params,
        )
    )


def get_external_entity(orcabus_id: str) -> ExternalEntityDetail:
    """
    Get a single external entity by its orcabus id.

    Uses the ``GET /api/v1/external-entity/{orcabusId}/`` endpoint.

    :param orcabus_id: The orcabus id of the external entity to retrieve.
    :return: The external entity object.
    """
    return cast(
        ExternalEntityDetail,
        get_case_request(
            endpoint=f"{EXTERNAL_ENTITY_ENDPOINT}/{orcabus_id}/",
        )
    )


# User
def list_users(params: Optional[Dict] = None) -> List[UserDetail]:
    """
    List all users.

    Uses the ``GET /api/v1/user/`` endpoint.

    :param params: Optional query parameters to filter the returned users.
    :return: A list of user objects.
    """
    return cast(
        List[UserDetail],
        get_case_request_response_results(
            endpoint=f"{USER_ENDPOINT}/",
            params=params,
        )
    )


def get_user(orcabus_id: str) -> UserDetail:
    """
    Get a single user by its orcabus id.

    Uses the ``GET /api/v1/user/{orcabusId}/`` endpoint.

    :param orcabus_id: The orcabus id of the user to retrieve.
    :return: The user object.
    """
    return cast(
        UserDetail,
        get_case_request(
            endpoint=f"{USER_ENDPOINT}/{orcabus_id}/",
        )
    )
