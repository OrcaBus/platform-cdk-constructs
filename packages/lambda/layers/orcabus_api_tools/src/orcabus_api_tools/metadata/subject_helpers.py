#!/usr/bin/env python3


"""
Helper functions for a subject
"""

# Standard imports
from typing import List
from requests import HTTPError

# Local imports
from . import get_metadata_request_response_results, get_item_objs_from_item_id_list
from .errors import SubjectNotFoundError
from .globals import SUBJECT_ENDPOINT, ORCABUS_ULID_REGEX_MATCH
from .models import Subject, Sample, LibraryDetail


def get_subject_from_subject_id(subject_id: str) -> Subject:
    """
    Get subject from the subject id
    :param subject_id:
    :return:
    """
    # We have an internal id, convert to int
    params = {
        "subject_id": subject_id
    }

    # Get subject
    try:
        query_results = get_metadata_request_response_results(SUBJECT_ENDPOINT, params)
        assert len(query_results) == 1
        return query_results[0]
    except (HTTPError, AssertionError):
        raise SubjectNotFoundError(
            subject_id=subject_id
        )


def get_subjects_list_from_subject_id_list(subject_id_list: List[str], accept_missing: bool = False) -> List[Sample]:
    """
    Get subject objects from subject id list
    :param subject_id_list:
    :return:
    """
    # We have an internal id, convert to int
    return list(map(
        lambda sample_iter_: Sample(**sample_iter_),
        get_item_objs_from_item_id_list(
            item_id_list=subject_id_list,
            item_identifier="subjectId",
            endpoint=SUBJECT_ENDPOINT,
            accept_missing=accept_missing
        )
    ))


def coerce_subject_id_or_orcabus_id_to_subject_orcabus_id(id_: str) -> str:
    if ORCABUS_ULID_REGEX_MATCH.match(id_):
        return id_
    else :
        return get_subject_orcabus_id_from_subject_id(id_)


def get_subject_orcabus_id_from_subject_id(subject_id: str) -> str:
    """
    Get the subject orcabus id from the subject id
    :param subject_id:
    :return:
    """
    return get_subject_from_subject_id(subject_id)['orcabusId']


def get_subjects_list_from_subject_orcabus_id_list(subject_orcabus_id_list: List[str], accept_missing: bool = False) -> List[Sample]:
    """
    Get subject objects from subject orcabus id list
    :param subject_orcabus_id_list:
    :return:
    """
    # We have an internal id, convert to int
    return list(map(
        lambda sample_iter_: Sample(**sample_iter_),
        get_item_objs_from_item_id_list(
            item_id_list=subject_orcabus_id_list,
            item_identifier="subjectId",
            endpoint=SUBJECT_ENDPOINT,
            accept_missing=accept_missing
        )
    ))


def get_subject_from_subject_orcabus_id(subject_orcabus_id: str) -> Subject:
    """
    Get subject from the subject id
    :param subject_orcabus_id:
    :return:
    """
    # Get subject id
    # We have an internal id, convert to int
    params = {
        "orcabus_id": subject_orcabus_id
    }

    # Get subject
    try:
        query_results = get_metadata_request_response_results(SUBJECT_ENDPOINT, params)
        assert len(query_results) == 1
        return query_results[0]
    except (HTTPError, AssertionError):
        raise SubjectNotFoundError(
            subject_orcabus_id=subject_orcabus_id
        )


def list_samples_in_subject(subject_orcabus_id: str) -> List[Sample]:
    """
    Given a subject id, list the samples in the subject
    :param subject_orcabus_id:
    :return:
    """
    from .sample_helpers import get_sample_from_sample_orcabus_id

    # Get the subject
    return list(map(
        # For each subject, get libraries in subject
        lambda library_iter_: get_sample_from_sample_orcabus_id(library_iter_['sample']['orcabusId']),
        # Get list of subject orcabus ids
        list_libraries_in_subject(subject_orcabus_id)
    ))


def list_libraries_in_subject(subject_orcabus_id: str) -> List[LibraryDetail]:
    """
    Given a subject id, return the list of library objects in the subject
    :param subject_orcabus_id:
    :return:
    """
    # Get ID For Subject
    subject = get_subject_from_subject_orcabus_id(subject_orcabus_id)

    # Get the subject
    return subject.get("librarySet", [])


def get_all_subjects() -> List[Subject]:
    """
    Get all subjects
    :return:
    """
    return get_metadata_request_response_results(SUBJECT_ENDPOINT)
