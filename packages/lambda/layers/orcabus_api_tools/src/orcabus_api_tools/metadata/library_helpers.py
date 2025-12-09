#!/usr/bin/env python
from functools import reduce
from operator import concat
from typing import Union, List

from requests import HTTPError

from .globals import LIBRARY_ENDPOINT, ORCABUS_ULID_REGEX_MATCH
from .models import Library, Subject, Contact, Project
from . import (
    get_metadata_request_response_results, get_item_objs_from_item_id_list
)
from .errors import LibraryNotFoundError


def get_library_from_library_id(library_id: str) -> Library:
    """
    Get library from the library id
    :param library_id:
    :return:
    """
    # Get library id
    # We have an internal id, convert to int
    params = {
        "library_id": library_id
    }

    # Get library
    try:
        query_results = get_metadata_request_response_results(LIBRARY_ENDPOINT, params)
        assert len(query_results) == 1
        return query_results[0]
    except (HTTPError, AssertionError) as e:
        raise LibraryNotFoundError(
            library_id=library_id,
        )


def get_libraries_list_from_library_id_list(library_id_list: List[str], accept_missing: bool = False) -> List[Library]:
    # We have an internal id, convert to int
    return list(map(
        lambda library_iter_: Library(**library_iter_),
        get_item_objs_from_item_id_list(
            item_id_list=library_id_list,
            item_identifier="libraryId",
            endpoint=LIBRARY_ENDPOINT,
            accept_missing=accept_missing
        )
    ))


def get_library_orcabus_id_from_library_id(library_id: str) -> str:
    """
    Get library from the library id
    :param library_id:
    :return:
    """
    # Get library id
    return get_library_from_library_id(library_id)['orcabusId']


def get_library_id_from_library_orcabus_id(library_id: str) -> str:
    """
    Get library from the library id
    :param library_id:
    :return:
    """
    # Get library id
    return get_library_from_library_orcabus_id(library_id)['libraryId']


def coerce_library_id_or_orcabus_id_to_library_orcabus_id(id_: str) -> str:
    if ORCABUS_ULID_REGEX_MATCH.match(id_):
        return id_
    else :
        return get_library_orcabus_id_from_library_id(id_)


def get_library_from_library_orcabus_id(library_orcabus_id: str) -> Library:
    """
    Get library from the library id
    :param library_orcabus_id:
    :return:
    """
    # Get library id
    # We have an internal id, convert to int
    params = {
        "orcabus_id": library_orcabus_id
    }

    # Get library
    try:
        query_list = get_metadata_request_response_results(LIBRARY_ENDPOINT, params)
        assert len(query_list) == 1
        return query_list[0]
    except (HTTPError, AssertionError) as e:
        raise LibraryNotFoundError(
            library_orcabus_id=library_orcabus_id,
        )


def get_libraries_from_library_orcabus_id_list(library_orcabus_id_list: List[str], accept_missing: bool = False) -> List[Library]:
    # We have an internal id, convert to int
    return list(map(
        lambda library_iter_: Library(**library_iter_),
        get_item_objs_from_item_id_list(
            item_id_list=library_orcabus_id_list,
            item_identifier="orcabusId",
            endpoint=LIBRARY_ENDPOINT,
            accept_missing=accept_missing
        )
    ))


def get_subject_from_library_id(library_id: str) -> Subject:
    """
    Given a library id, collect the subject id
    :param library_id:
    :return:
    """
    from .subject_helpers import get_subject_from_subject_orcabus_id

    # Get the subject linked to this library id
    subject_orcabus_id = get_library_from_library_id(library_id)["subject"]["orcabusId"]

    return get_subject_from_subject_orcabus_id(subject_orcabus_id)


def get_library_type(library_id: str) -> Union[str | None]:
    """
    Given a library id, collect the library id type
    :param library_id:
    :return:
    """
    library = get_library_from_library_id(library_id)

    return library.get("type")


def get_library_assay_type(library_id: str) -> Union[str | None]:
    """
    Given a library id, collect the library assay type
    :param library_id:
    :return:
    """
    library = get_library_from_library_id(library_id)

    return library.get("assay")


def get_library_phenotype(library_id: str) -> Union[str | None]:
    """
    Given a library id, collect the library phenotype
    :param library_id:
    :return:
    """
    library = get_library_from_library_id(library_id)

    return library.get("phenotype")


def get_library_workflow(library_id: str) -> Union[str | None]:
    """
    Given a library id, collect the library workflow
    :param library_id:
    :return:
    """
    library = get_library_from_library_id(library_id)

    return library.get("workflow")


def get_all_libraries() -> List[Library]:
    """
    Collect all libraries from the database
    :return:
    """
    return get_metadata_request_response_results(LIBRARY_ENDPOINT)


def get_project_list_from_library_orcabus_id(library_orcabus_id: str) -> List[Project]:
    """
    Given a library orcabus id, collect the project list
    :param library_orcabus_id:
    :return:
    """
    # Local imports
    from .project_helpers import get_project_from_project_orcabus_id

    # For each project in the projectSet, get the project (convert from ProjectDetail to Project)
    # Then return the list
    return list(map(
        lambda project_iter_: get_project_from_project_orcabus_id(project_iter_['orcabusId']),
        get_library_from_library_orcabus_id(library_orcabus_id)["projectSet"]
    ))


def get_project_list_from_library_id(library_id: str) -> List[Project]:
    """
    Given a library id, collect the project list
    :param library_id:
    :return:
    """
    return get_project_list_from_library_orcabus_id(get_library_orcabus_id_from_library_id(library_id))


def get_contact_list_from_library_orcabus_id(library_orcabus_id: str) -> List[Contact]:
    """
    Given a library orcabus id, collect the contact list
    :param library_orcabus_id:
    :return:
    """
    # Local imports
    from .project_helpers import get_project_from_project_orcabus_id
    from .contact_helpers import get_contact_from_contact_orcabus_id

    # For each project in the projectSet,
    # Get the contact set, then we reduce to a single list
    contact_list = list(reduce(
        concat,
        list(map(
            lambda project_iter_: get_project_from_project_orcabus_id(project_iter_['orcabusId'])['contactSet'],
            get_library_from_library_orcabus_id(library_orcabus_id)["projectSet"]
        ))
    ))

    # We need to deduplicate the contact list
    contact_list = list({contact_iter_['orcabusId']: contact_iter_ for contact_iter_ in contact_list}.values())

    # Then convert from ContactDetail to Contact objects by fetching each contact
    contact_list = list(map(
        lambda contact_iter_: get_contact_from_contact_orcabus_id(contact_iter_['orcabusId']),
        contact_list
    ))

    return contact_list


def get_contact_list_from_library_id(library_id: str) -> List[Contact]:
    """
    Given a library id, collect the contact list
    :param library_id:
    :return:
    """
    return get_contact_list_from_library_orcabus_id(get_library_orcabus_id_from_library_id(library_id))
