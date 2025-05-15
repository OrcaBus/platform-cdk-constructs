#!/usr/bin/env python3
from .globals import SEQUENCE_SUBDOMAIN_NAME
from .models import Sequence, SequenceDetail, SampleSheet
from ..utils.requests_helpers import get_request_response_results, get_request, get_url


def get_sequence_url(endpoint: str) -> str:
    """
    Get the URL for the Metadata endpoint
    :param endpoint:
    :return:
    """
    return get_url(
        endpoint,
        SEQUENCE_SUBDOMAIN_NAME
    )

def get_sequence_object_from_instrument_run_id(instrument_run_id: str) -> SequenceDetail:
    """
    Get the sequence object from the instrument run id.
    :param instrument_run_id:
    :return:
    """

    return Sequence(
        **dict(
            get_request_response_results(
                get_sequence_url(endpoint="api/v1/sequence"),
                params={
                    "instrumentRunId": instrument_run_id,
                }
            )[0]
        )
    )


def get_sample_sheet_from_orcabus_id(sequence_orcabus_id: str) -> SampleSheet:
    """
    Get the sample sheet from the orcabus id.
    :param sequence_orcabus_id:
    :return:
    """

    return SampleSheet(
        **dict(
            get_request(
                get_sequence_url(endpoint=f"api/v1/sequence/{sequence_orcabus_id}/sample_sheet")
            )
        )
    )


def get_library_ids_in_sequence(sequence_orcabus_id: str) -> list[str]:
    """
    Get the library ids in the sequence run.
    :param sequence_orcabus_id:
    :return:
    """

    return get_request(
        get_sequence_url(endpoint=f"api/v1/sequence/{sequence_orcabus_id}")
    )['libraries']
