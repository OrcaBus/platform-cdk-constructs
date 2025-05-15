#!/usr/bin/env python3


# !/usr/bin/env python3


"""
Helper functions for a subject
"""

# Standard imports
from typing import List
from requests.exceptions import HTTPError

# Local imports
from . import get_metadata_request_response_results, get_item_objs_from_item_id_list
from .errors import SampleNotFoundError
from .globals import SAMPLE_ENDPOINT, ORCABUS_ULID_REGEX_MATCH
from .models import Sample, LibraryDetail



def get_sample_from_sample_id(sample_id: str) -> Sample:
    """
    Get sample from the sample id
    :param sample_id:
    :return:
    """
    # We have an internal id
    params = {
        "sampleId": sample_id
    }

    # Get sample
    try:
        query_results = get_metadata_request_response_results(SAMPLE_ENDPOINT, params)
        assert len(query_results) == 1
        return query_results[0]
    except (HTTPError, AssertionError):
        raise SampleNotFoundError(
            sample_id=sample_id
        )


def get_samples_list_from_sample_id_list(sample_id_list: List[str], accept_missing: bool = False) -> List[Sample]:
    """
    Get sample from the sample id
    :param sample_id:
    :return:
    """
    # We have an internal id, convert to int
    return list(map(
        lambda sample_iter_: Sample(**sample_iter_),
        get_item_objs_from_item_id_list(
            item_id_list=sample_id_list,
            item_identifier="sampleId",
            endpoint=SAMPLE_ENDPOINT,
            accept_missing=accept_missing
        )
    ))


def get_sample_orcabus_id_from_sample_id(sample_id: str) -> str:
    return get_sample_from_sample_id(sample_id)["orcabusId"]


def get_sample_from_sample_orcabus_id(sample_orcabus_id: str) -> Sample:
    """
    Get sample from the sample id
    :param sample_orcabus_id:
    :return:
    """
    # We have an internal id
    params = {
        "orcabusId": sample_orcabus_id
    }

    # Get sample
    try:
        query_results = get_metadata_request_response_results(SAMPLE_ENDPOINT, params)
        assert len(query_results) == 1
        return query_results[0]
    except (HTTPError, AssertionError):
        raise SampleNotFoundError(
            sample_orcabus_id=sample_orcabus_id
        )


def get_samples_list_from_sample_orcabus_id_list(sample_orcabus_id_list: List[str], accept_missing: bool = False) -> List[Project]:
    """
    Get sample from the sample id
    :param sample_id:
    :return:
    """
    # We have an internal id, convert to int
    return list(map(
        lambda sample_iter_: Sample(**sample_iter_),
        get_item_objs_from_item_id_list(
            item_id_list=sample_orcabus_id_list,
            item_identifier="orcabusId",
            endpoint=SAMPLE_ENDPOINT,
            accept_missing=accept_missing
        )
    ))


def coerce_sample_id_or_orcabus_id_to_sample_orcabus_id(id_: str) -> str:
    if ORCABUS_ULID_REGEX_MATCH.match(id_):
        return id_
    else :
        return get_sample_orcabus_id_from_sample_id(id_)


def list_libraries_in_sample(sample_orcabus_id: str) -> List[LibraryDetail]:
    """
    Given a sample id, return the list of library objects in the sample
    :param sample_orcabus_id:
    :return:
    """
    # Get ID For Subject
    sample = get_sample_from_sample_orcabus_id(sample_orcabus_id)

    # Get the sample
    return sample.get("librarySet", [])


def get_all_samples():
    """
    Get all samples from the sample database
    :return:
    """
    return get_metadata_request_response_results(SAMPLE_ENDPOINT)
