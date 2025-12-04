#!/usr/bin/env python3
import warnings
# Standard imports
from typing import Optional, cast, List
import logging


# Local imports
from . import get_sequence_request
from .globals import SEQUENCE_RUN_ENDPOINT, SEQUENCE_ENDPOINT
from .models import SequenceDetail, SampleSheet, Sequence


def get_sample_sheet_from_instrument_run_id(instrument_run_id: str) -> Optional[SampleSheet]:
    samplesheet_dict_list = sorted(
        get_sequence_request(endpoint=f"{SEQUENCE_ENDPOINT}/{instrument_run_id}/sample_sheets"),
        key=lambda x: x.get("orcabusId")
    )

    if len(samplesheet_dict_list) == 0:
        logging.warning("Could not find sample sheet for instrument run id: %s", instrument_run_id)
        return None

    # If there are multiple sample sheets, print to logs, but return the last one
    if len(samplesheet_dict_list) > 1:
        logging.warning(
            f"Multiple sample sheets found for instrument run id {instrument_run_id}. "
            f"Returning the last one."
        )

    return cast(SampleSheet, samplesheet_dict_list[-1])


def get_library_id_list_from_instrument_run_id(instrument_run_id: str) -> List[str]:
    """
    Get the sequence run object
    :param instrument_run_id:
    :return:
    """
    sequence_run_object = get_sequence_object_from_instrument_run_id(
        instrument_run_id=instrument_run_id
    )

    if sequence_run_object is None:
        logging.warning("Could not find sequence run for instrument run id: %s", instrument_run_id)
        return []

    return list(set(sequence_run_object.get('libraries', [])))


def get_library_id_list_in_sequence(sequence_orcabus_id: str) -> List[str]:
    """
    Get the library ids in the sequence run.
    :param sequence_orcabus_id:
    :return:
    """
    return list(set(get_sequence_request(endpoint=f"{SEQUENCE_RUN_ENDPOINT}/{sequence_orcabus_id}").get('libraries', [])))


def get_library_ids_in_sequence(sequence_orcabus_id: str) -> List[str]:
    warnings.warn(DeprecationWarning(
        "get_library_ids_in_sequence is deprecated. Use get_library_id_list_in_sequence instead."
    ))
    return get_library_id_list_in_sequence(sequence_orcabus_id=sequence_orcabus_id)


def get_libraries_from_instrument_run_id(instrument_run_id: str) -> List[str]:
    warnings.warn(DeprecationWarning(
        "get_libraries_from_instrument_run_id is deprecated. Use get_library_id_list_from_instrument_run_id instead."
    ))
    return get_library_id_list_from_instrument_run_id(instrument_run_id=instrument_run_id)


def get_sequence_object_from_instrument_run_id(instrument_run_id: str) -> Optional[Sequence]:
    """
    Get the sequence object from the instrument run id.
    :param instrument_run_id:
    :return:
    """

    # Get the sequence run details from the instrument run id
    sequence_run_dict_list = sorted(
        get_sequence_request(endpoint=f"{SEQUENCE_ENDPOINT}/{instrument_run_id}/sequence_run"),
        # Orcabus ids are ulids so they are sortable by timestamp
        key=lambda x: x.get("orcabusId")
    )

    # Check we have at least one sequence run
    if len(sequence_run_dict_list) == 0:
        logging.warning("Could not find sequence run for instrument run id: %s", instrument_run_id)
        return None

    # Check if there are multiple sequence runs
    if len(sequence_run_dict_list) > 1:
        logging.warning(
            f"Multiple sequence runs found for instrument run id {instrument_run_id}. "
            f"Returning the last one that has a sequenceRunName"
        )
        return cast(Sequence, next(filter(
            lambda sequence_run_iter_: (
                sequence_run_iter_.get('sequenceRunName') is not None
            ),
            reversed(sequence_run_dict_list)
        )))

    # Return the first (and only) sequence run
    return cast(Sequence, sequence_run_dict_list[0])


def get_sample_sheet_from_orcabus_id(sequence_orcabus_id: str) -> SampleSheet:
    """
    Get the sample sheet from the orcabus id.
    :param sequence_orcabus_id:
    :return:
    """

    return SampleSheet(
        **dict(
            get_sequence_request(endpoint=f"{SEQUENCE_RUN_ENDPOINT}/{sequence_orcabus_id}/sample_sheet")
        )
    )


