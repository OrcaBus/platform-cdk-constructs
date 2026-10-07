#!/usr/bin/env python3

"""
Interact with the SRM service
"""

# Standard imports
from pathlib import Path
import warnings
from typing import Optional, cast, List, Dict
import logging

# Local imports
from . import get_sequence_request, sequence_post_request
from .globals import SEQUENCE_RUN_ENDPOINT, SEQUENCE_ENDPOINT
from .models import SampleSheet, Sequence


def list_sample_sheets_for_instrument_run_id(
        instrument_run_id: str,
) -> Optional[List[SampleSheet]]:
    samplesheet_dict_list = sorted(
        get_sequence_request(endpoint=f"{SEQUENCE_ENDPOINT}/{instrument_run_id}/sample_sheets"),
        key=lambda x: x.get("orcabusId")
    )

    if len(samplesheet_dict_list) == 0:
        logging.warning("Could not find sample sheet for instrument run id: %s", instrument_run_id)
        return None

    return samplesheet_dict_list


def get_sample_sheet_from_instrument_run_id(
        instrument_run_id: str,
        sequence_run_id: Optional[str] = None
) -> Optional[SampleSheet]:
    samplesheet_dict_list = list_sample_sheets_for_instrument_run_id(
        instrument_run_id=instrument_run_id
    )

    # None?
    if samplesheet_dict_list is None:
        logging.warning("Could not find sample sheet for instrument run id: %s", instrument_run_id)
        return None

    # Only one? Well that's the one
    if len(samplesheet_dict_list) == 1:
        return samplesheet_dict_list[0]

    # Multiple, check based on Sequence
    if sequence_run_id is not None:
        samplesheet_match = next(
            filter(
                lambda samplesheet_iter_: samplesheet_iter_['sequence'] == sequence_run_id,
                samplesheet_dict_list
            ),
            None
        )
        if samplesheet_match is not None:
            return samplesheet_match

    # If there are multiple sample sheets, print to logs, but return the last one
    if len(samplesheet_dict_list) > 1:
        logging.warning(
            f"Multiple sample sheets found for instrument run id {instrument_run_id}. "
            f"Returning the last one."
        )

    return samplesheet_dict_list[-1]


def get_library_id_list_from_instrument_run_id(
        instrument_run_id: str,
        sequence_run_id: Optional[str] = None,
) -> List[str]:
    """
    Get the sequence run object
    :param instrument_run_id:
    :param sequence_run_id:
    :return:
    """
    sequence_run_object = get_sequence_object_from_instrument_run_id(
        instrument_run_id=instrument_run_id,
        sequence_run_id=sequence_run_id,
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


def get_sequence_object_from_instrument_run_id(
        instrument_run_id: str,
        sequence_run_id: Optional[str] = None,
) -> Optional[Sequence]:
    """
    Get the sequence object from the instrument run id.
    :param instrument_run_id:
    :param sequence_run_id:
    :return:
    """

    # Get the sequence run details from the instrument run id
    sequence_run_dict_list = sorted(
        get_sequence_request(endpoint=f"{SEQUENCE_ENDPOINT}/{instrument_run_id}/sequence_run"),
        # Orcabus ids are ulids so they are sortable by timestamp
        key=lambda x: x.get("orcabusId"),
        # And we want the latest
        reverse=True
    )

    # Check we have at least one sequence run
    if len(sequence_run_dict_list) == 0:
        logging.warning("Could not find sequence run for instrument run id: %s", instrument_run_id)
        return None

    if len(sequence_run_dict_list) == 1:
        return cast(Sequence, sequence_run_dict_list[0])

    # Check if there are multiple sequence runs
    logging.warning(
        f"Multiple sequence runs found for instrument run id {instrument_run_id}. "
        f"Returning the last one that has a sequenceRunName"
    )

    # Try finding a matching sequence run id
    if sequence_run_id is not None:
        sequence_run_match = next(
            filter(
                lambda sequence_run_iter_: (
                    sequence_run_iter_.get('sequenceRunId') == sequence_run_id
                ),
                sequence_run_dict_list
            ),
            None
        )
        if sequence_run_match is not None:
            return cast(Sequence, sequence_run_match)

    # Get the latest one with a sequence run name
    sequence_run_with_name = next(
        filter(
            lambda sequence_run_iter_: (
                sequence_run_iter_.get('sequenceRunName') is not None
            ),
            sequence_run_dict_list
        ),
        None
    )
    if sequence_run_with_name is None:
        logging.warning(
            "None of the sequence runs for instrument run id %s had a sequenceRunName",
            instrument_run_id
        )
        return None

    return cast(Sequence, sequence_run_with_name)


def get_sequence_run_object_from_sequence_orcabus_id(sequence_orcabus_id: str) -> Sequence:
    return get_sequence_request(endpoint=f"{SEQUENCE_RUN_ENDPOINT}/{sequence_orcabus_id}")
    

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


def add_samplesheet(
        instrument_run_id: str,
        samplesheet_path: Path,
        created_by: str,
        comment: str
) -> Dict:
    """
    Add a sample sheet to the sequence run.
    :param instrument_run_id: The instrument run identifier for which the sample sheet is being added.
    :param samplesheet_path: Path to the sample sheet file to be uploaded.
    :param created_by: The user who is adding the sample sheet.
    :param comment: A comment describing the sample sheet or the reason for adding it.
    :return: Response from the API containing the updated sequence information.
    """
    # Open the sample sheet file
    with open(samplesheet_path, 'rb') as file_data:
        return sequence_post_request(
            endpoint=f"{SEQUENCE_RUN_ENDPOINT}/action/add_samplesheet/",
            files={
                "file": ("SampleSheet.csv", file_data, 'text/csv'),
                "instrument_run_id": (None, instrument_run_id),
                "created_by": (None, created_by),
                "comment": (None, comment),
            }
        )
