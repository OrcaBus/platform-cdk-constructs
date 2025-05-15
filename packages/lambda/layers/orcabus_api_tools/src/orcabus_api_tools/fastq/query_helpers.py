#!/usr/bin/env python3

"""
Query helpers -

get_fastqs_in_instrument_run_id

get_fastqs_in_library

get_fastqs_in_sample

get_fastqs_in_subject

get_fastqs_in_individual

get_fastqs_in_project

get_fastq_by_rgid_and_instrument_run_id

"""
from functools import reduce
from itertools import batched
from operator import concat
from typing import List, Unpack

from . import get_fastq_request_response_results, get_fastq_request
from .globals import FASTQ_LIST_ROW_ENDPOINT, FASTQ_SET_ENDPOINT
from .models import FastqListRow, FastqSet, Job, FastqListRowQueryParameters, FastqSetQueryParameters, \
    FastqGetResponseParameters, VALID_BATCH_KEYS


def get_fastq(fastq_id: str, **kwargs: Unpack[FastqGetResponseParameters]) -> FastqListRow:
    # Raise error if any of the kwargs are not in the FastqSetQueryParameters
    for key in kwargs.keys():
        if key not in FastqGetResponseParameters.__annotations__:
            raise ValueError(f"Invalid parameter: {key}")

    return FastqListRow(
        **get_fastq_request(
            f"{FASTQ_LIST_ROW_ENDPOINT}/{fastq_id}",
            params=dict(kwargs)
        )
    )


def get_fastq_set(
        fastq_set_id: str,
        **kwargs: Unpack[FastqGetResponseParameters]
) -> FastqSet:
    """
    Get the fastq set by id
    :param fastq_set_id:
    :param kwargs:
    :return:
    """
    # Raise error if any of the kwargs are not in the FastqSetQueryParameters
    for key in kwargs.keys():
        if key not in FastqSetQueryParameters.__annotations__:
            raise ValueError(f"Invalid parameter: {key}")

    return FastqSet(
        **get_fastq_request(
            f"{FASTQ_SET_ENDPOINT}/{fastq_set_id}",
            params=dict(kwargs)
        )
    )


def get_fastqs(**kwargs: Unpack[FastqListRowQueryParameters]) -> List[FastqListRow]:
    """
    Get all fastqs
    """
    # Raise error if any of the kwargs are not in the FastqListRowQueryParameters
    for key in kwargs.keys():
        if key not in FastqListRowQueryParameters.__annotations__:
            raise ValueError(f"Invalid parameter: {key}")

    return get_fastq_request_response_results(
        FASTQ_LIST_ROW_ENDPOINT,
        params=dict(kwargs)
    )


def get_fastq_sets(**kwargs: Unpack[FastqSetQueryParameters]) -> List[FastqSet]:
    """
    Get the fastq set
    :param args:
    :param kwargs:
    :return:
    """
    # Raise error if any of the kwargs are not in the FastqListRowQueryParameters
    for key in kwargs.keys():
        if key not in FastqSetQueryParameters.__annotations__:
            raise ValueError(f"Invalid parameter: {key}")

    return get_fastq_request_response_results(
        FASTQ_SET_ENDPOINT,
        params=dict(kwargs)
    )


def get_fastqs_in_instrument_run_id(instrument_run_id: str):
    """
    Get all fastqs in an instrument run id
    """
    return get_fastqs(
        instrumentRunId=instrument_run_id
    )


def get_fastqs_in_library(library_id: str):
    """
    Get all fastqs in a library
    """
    return get_fastqs(
        library=library_id,
    )


def get_fastqs_batched(
        item_key: VALID_BATCH_KEYS,
        item_list: List[str],
        batch_size: int = 100,
        **kwargs
) -> List[FastqListRow]:
    """
    Get all fastqs in a list of libraries
    """
    # Split by groups of 50
    item_lists = batched(item_list, batch_size)

    # Get the s3 objects
    try:
        return list(reduce(
            concat,
            list(map(
                lambda item_batch_:
                get_fastqs(
                    **{
                        f"{item_key}[]": list(item_batch_),
                    },
                    **kwargs,
                    rowsPerPage=100
                ),
                item_lists
            ))
        ))
    except TypeError as e:
        # TypeError: reduce() of empty iterable with no initial value
        return []


def get_fastqs_in_library_list(
        library_id_list: List[str]
) -> List[FastqListRow]:
    """
    Get all fastqs in a list of libraries
    """
    return get_fastqs_batched(
        item_key="library",
        item_list=library_id_list,
        batch_size=50
    )


def get_fastqs_in_libraries_and_instrument_run_id(library_id_list, instrument_run_id):
    """
    Get all fastqs in a list of libraries and instrument run id
    :param library_id_list:
    :param instrument_run_id:
    :return:
    """
    return get_fastqs(
        instrumentRunId=instrument_run_id,
        **{
            "library[]": library_id_list,
        }
    )


def get_fastqs_in_sample(sample_id: str):
    """
    Get all fastqs in a sample
    """
    return get_fastqs(
        sample=sample_id
    )


def get_fastqs_in_sample_list(sample_id_list: List[str]):
    """
    Get all fastqs in a list of samples
    :param sample_id_list:
    :return:
    """
    return get_fastqs_batched(
        item_key="sample",
        item_list=sample_id_list,
        batch_size=50
    )


def get_fastqs_in_subject(subject_id):
    """
    Get all fastqs in a subject
    """
    return get_fastqs(
        subject=subject_id
    )


def get_fastqs_in_individual(individual_id):
    """
    Get all fastqs in an individual
    """
    return get_fastqs(
        individual=individual_id
    )


def get_fastqs_in_project(project_id):
    """
    Get all fastqs in a project
    """
    return get_fastqs(
        project=project_id
    )


def get_fastq_list_rows_in_fastq_set(fastq_set_id):
    """
    Get all fastqs in a fastq set
    """
    return get_fastqs(
        fastqSetId=fastq_set_id
    )


def get_fastq_jobs(fastq_id: str) -> List[Job]:
    """
    Get all fastqs in a fastq set
    """
    return list(map(
        lambda job_iter_: Job(**job_iter_),
        get_fastq_request_response_results(
            f"{FASTQ_LIST_ROW_ENDPOINT}/{fastq_id}/jobs"
        )
    ))
