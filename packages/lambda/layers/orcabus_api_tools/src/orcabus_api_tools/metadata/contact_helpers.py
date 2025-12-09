#!/usr/bin/env python3

"""
Helpers for using the contact API endpoint
"""
# Standard imports
from functools import reduce
from operator import concat
from typing import List
from requests import HTTPError

# Local imports
from . import get_metadata_request_response_results, get_item_objs_from_item_id_list
from .globals import CONTACT_ENDPOINT, ORCABUS_ULID_REGEX_MATCH
from .models import Contact, Library
from .errors import ContactNotFoundError


def get_contact_from_contact_id(contact_id: str) -> Contact:
    """
    Get contact from the contact id
    :param contact_id:
    :return:
    """
    # We have an internal id, convert to int
    params = {
        "contactId": contact_id
    }

    # Get contact
    try:
        query_list = get_metadata_request_response_results(CONTACT_ENDPOINT, params)
        assert len(query_list) == 1
        return query_list[0]
    except (HTTPError, AssertionError):
        raise ContactNotFoundError(
            contact_id=contact_id,
        )


def get_contacts_list_from_contact_id_list(contact_id_list: List[str], accept_missing=False) -> List[Contact]:
    """
    Given a list of contact ids, return a list of Contact objects
    :param contact_id_list:
    :param accept_missing:
    :return:
    """
    # We have an internal id, convert to int
    return list(map(
        lambda contact_iter_: Contact(**contact_iter_),
        get_item_objs_from_item_id_list(
            item_id_list=contact_id_list,
            item_identifier="contactId",
            endpoint=CONTACT_ENDPOINT,
            accept_missing=accept_missing
        )
    ))


def get_contact_orcabus_id_from_contact_id(contact_id: str) -> str:
    return get_contact_from_contact_id(contact_id)['orcabusId']


def get_contact_from_contact_orcabus_id(contact_orcabus_id: str) -> Contact:
    """
    Get contact from the contact id
    :param contact_orcabus_id:
    :return:
    """
    params = {
        "orcabusId": contact_orcabus_id.split(".")[1]
    }

    # Get contact
    try:
        query_result = get_metadata_request_response_results(CONTACT_ENDPOINT, params)
        assert len(query_result) == 1
        return query_result[0]
    except (HTTPError, AssertionError):
        raise ContactNotFoundError(
            contact_orcabus_id=contact_orcabus_id,
        )


def get_contacts_list_from_contact_orcabus_id_list(contact_orcabus_id_list: List[str], accept_missing=False) -> List[Contact]:
    # We have an internal id, convert to int
    return list(map(
        lambda contact_iter_: Contact(**contact_iter_),
        get_item_objs_from_item_id_list(
            item_id_list=contact_orcabus_id_list,
            item_identifier="orcabusId",
            endpoint=CONTACT_ENDPOINT,
            accept_missing=accept_missing
        )
    ))


def coerce_contact_id_or_orcabus_id_to_contact_orcabus_id(id_: str) -> str:
    if ORCABUS_ULID_REGEX_MATCH.match(id_):
        return id_
    else :
        return get_contact_orcabus_id_from_contact_id(id_)


def get_all_contacts() -> List[Contact]:
    """
    Get all subjects
    :return:
    """
    return get_metadata_request_response_results(CONTACT_ENDPOINT)


def list_libraries_for_contact_orcabus_id(contact_orcabus_id: str) -> List[Library]:
    """
    Given a contact orcabus id, get libraries associated with projects, associated with the contact
    :param contact_orcabus_id:
    :return:
    """
    from .project_helpers import list_libraries_in_project

    # Get the contact object
    contact_obj = get_contact_from_contact_orcabus_id(contact_orcabus_id)

    # For each project in the projectSet, get the libraries in the project
    library_object_list = list(reduce(
        concat,
        list(map(
            lambda project_iter_: list_libraries_in_project(project_iter_['orcabusId']),
            contact_obj.get('projectSet', [])
        )),
        []
    ))

    # Remove duplicates by library orcabus id
    library_object_list = list({lib['orcabusId']: lib for lib in library_object_list}.values())

    return library_object_list


def list_libraries_for_contact_id(contact_id: str) -> List[Library]:
    """
    Get libraries associated with a contact id
    :param contact_id:
    :return:
    """
    return list_libraries_for_contact_orcabus_id(
        get_contact_orcabus_id_from_contact_id(contact_id)
    )
