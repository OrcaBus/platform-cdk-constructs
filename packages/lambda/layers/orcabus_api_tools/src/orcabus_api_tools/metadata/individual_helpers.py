#!/usr/bin/env python3

"""
This module contains helper functions for the individual class.
"""

# Standard imports
from typing import List
from requests import HTTPError
from functools import reduce
from operator import concat

# Local imports
from . import get_metadata_request_response_results, get_item_objs_from_item_id_list
from .models import Individual, LibraryDetail
from .errors import IndividualNotFoundError
from .globals import INDIVIDUAL_ENDPOINT, ORCABUS_ULID_REGEX_MATCH


def get_individual_from_individual_id(individual_id: str) -> Individual:
    """
    Get individual from the individual id
    :param individual_id:
    :return:
    """
    # We have an internal id
    params = {
        "individual_id": individual_id
    }

    # Get individual
    try:
        query_results = get_metadata_request_response_results(INDIVIDUAL_ENDPOINT, params)
        assert len(query_results) == 1
        return query_results[0]
    except (HTTPError, AssertionError):
        raise IndividualNotFoundError(
            individual_id=individual_id
        )


def get_individuals_list_from_individual_id_list(individual_id_list: List[str], accept_missing=False) -> List[Individual]:
    """
    Get individual from the individual id list
    :param accept_missing:
    :param individual_id_list:
    :return:
    """
    # We have an internal id, convert to int
    return list(map(
        lambda individual_iter_: Individual(**individual_iter_),
        get_item_objs_from_item_id_list(
            item_id_list=individual_id_list,
            item_identifier="individualId",
            endpoint=INDIVIDUAL_ENDPOINT,
            accept_missing=accept_missing
        )
    ))


def get_individual_orcabus_id_from_individual_id(individual_id: str) -> str:
    return get_individual_from_individual_id(individual_id)["orcabusId"]


def get_individual_from_individual_orcabus_id(individual_orcabus_id: str) -> Individual:
    """
    Get individual from the individual id
    :param individual_orcabus_id:
    :return:
    """
    # We have an internal id
    params = {
        "orcabus_id": individual_orcabus_id
    }

    # Get individual
    try:
        query_results = get_metadata_request_response_results(INDIVIDUAL_ENDPOINT, params)
        assert len(query_results) == 1
        return query_results[0]
    except (HTTPError, AssertionError):
        raise IndividualNotFoundError(
            individual_orcabus_id=individual_orcabus_id
        )


def get_individuals_list_from_individual_orcabus_id_list(individual_orcabus_id_list: List[str], accept_missing=False) -> List[Individual]:
    """
    Get individual from the individual id list
    :param accept_missing:
    :param individual_orcabus_id_list:
    :return:
    """
    # We have an internal id, convert to int
    return list(map(
        lambda individual_iter_: Individual(**individual_iter_),
        get_item_objs_from_item_id_list(
            item_id_list=individual_orcabus_id_list,
            item_identifier="orcabusId",
            endpoint=INDIVIDUAL_ENDPOINT,
            accept_missing=accept_missing
        )
    ))


def coerce_individual_id_or_orcabus_id_to_individual_orcabus_id(id_: str) -> str:
    if ORCABUS_ULID_REGEX_MATCH.match(id_):
        return id_
    else :
        return get_individual_orcabus_id_from_individual_id(id_)


def get_all_individuals():
    """
    Get all samples from the sample database
    :return:
    """
    return get_metadata_request_response_results(INDIVIDUAL_ENDPOINT)


def list_libraries_in_individual(individual_orcabus_id: str) -> List[LibraryDetail]:
    """
    Given an individual id, return all the libraries associated with the individual
    First we need to collect all subjects associated with the individual
    Then we need to collect all libraries associated with the subjects

    :param individual_orcabus_id:
    :return:
    """
    from .subject_helpers import list_libraries_in_subject
    return list(reduce(
        concat,
        list(map(
            # For each subject, get libraries in subject
            lambda subject_iter_: list_libraries_in_subject(subject_iter_['orcabusId']),
            # Get list of subject orcabus ids
            get_individual_from_individual_orcabus_id(individual_orcabus_id)["subjectSet"]
        ))
    ))
