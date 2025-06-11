#!/usr/bin/env python3

"""
Update helpers for the update script.

- add_qc_stats
- add_read_count
- add_ntsm_storage_object / add_ntsm
- add_fastq_pair_storage_object / add_read_set
- detach_fastq_pair_storage_object / detach_read_set
- validate
- invalidate
"""
# Standard imports

# Local imports
from . import fastq_patch_request
from .globals import FASTQ_LIST_ROW_ENDPOINT, FASTQ_SET_ENDPOINT
from .models import (
    QcStats, FastqListRow, ReadCount,
    FileCompressionInformation, FileStorageObject, ReadSet,
    FastqSet
)


def add_qc_stats(fastq_id: str, qc_stats: QcStats) -> FastqListRow:
    """
    Add QC stats to a fastq_id.

    :param fastq_id: Fastq str
    :param qc_stats: Dictionary of QC stats
    """
    # Raise error if any of the kwargs are not in the QcStats
    for key in qc_stats.keys():
        if key not in QcStats.__annotations__:
            raise ValueError(f"Invalid parameter: {key}")

    return fastq_patch_request(
        f"{FASTQ_LIST_ROW_ENDPOINT}/{fastq_id}/addQcStats",
        params=dict(qc_stats)
    )


def add_read_count(fastq_id: str, read_count: ReadCount) -> FastqListRow:
    """
    Add read count to a fastq id
    :param fastq_id:
    :param read_count:
    :return:
    """
    for key in read_count.keys():
        if key not in ReadCount.__annotations__:
            raise ValueError(f"Invalid parameter: {key}")

    return fastq_patch_request(
        f"{FASTQ_LIST_ROW_ENDPOINT}/{fastq_id}/addReadCount",
        params=dict(read_count)
    )


def add_file_compression_information(fastq_id: str, file_compression_information: FileCompressionInformation) -> FastqListRow:
    """
    Add file compression information to a fastq id
    :param fastq_id:
    :param file_compression_information:
    :return:
    """
    for key in file_compression_information.keys():
        if key not in FileCompressionInformation.__annotations__:
            raise ValueError(f"Invalid parameter: {key}")

    return fastq_patch_request(
        f"{FASTQ_LIST_ROW_ENDPOINT}/{fastq_id}/addFileCompressionInformation",
        params=dict(file_compression_information)
    )


def add_ntsm_storage_object(fastq_id: str, ntsm_fastq_storage_object: FileStorageObject) -> FastqListRow:
    """
    Add a Ntsm storage object to a fastq id.

    :param fastq_id: Fastq str
    :param ntsm_fastq_storage_object: Ntsm str
    """
    for key in ntsm_fastq_storage_object.keys():
        if key not in FileStorageObject.__annotations__:
            raise ValueError(f"Invalid parameter: {key}")

    return fastq_patch_request(
        f"{FASTQ_LIST_ROW_ENDPOINT}/{fastq_id}/addNtsmStorageObject",
        params=dict(ntsm_fastq_storage_object)
    )


def add_read_set(fastq_id: str, read_set: ReadSet) -> FastqListRow:
    """
    Add a read set to a fastq id.

    :param fastq_id: Fastq str
    :param read_set: ReadSet str
    """
    for key in read_set.keys():
        if key not in ReadSet.__annotations__:
            raise ValueError(f"Invalid parameter: {key}")

    return fastq_patch_request(
        f"{FASTQ_LIST_ROW_ENDPOINT}/{fastq_id}/addFastqPairStorageObject",
        params=dict(read_set)
    )


def detach_read_set(fastq_id: str) -> FastqListRow:
    """
    Detach a read set to a fastq id.

    :param fastq_id: Fastq str
    """
    return fastq_patch_request(
        f"{FASTQ_LIST_ROW_ENDPOINT}/{fastq_id}/detachFastqPairStorageObject"
    )


def validate_fastq(fastq_id: str) -> FastqListRow:
    """
    Validate a fastq id.

    :param fastq_id: Fastq str
    """
    return fastq_patch_request(
        f"{FASTQ_LIST_ROW_ENDPOINT}/{fastq_id}/validate"
    )


def invalidate_fastq(fastq_id: str) -> FastqListRow:
    """
    Invalidate a fastq id.

    :param fastq_id: Fastq str
    """
    return fastq_patch_request(
        f"{FASTQ_LIST_ROW_ENDPOINT}/{fastq_id}/invalidate"
    )


def link_fastq_list_row_to_fastq_set(fastq_id: str, fastq_set_id: str) -> FastqSet:
    """
    Link a fastq id to a fastq set.

    :param fastq_id:
    :param fastq_set_id:
    :return:
    """
    return fastq_patch_request(
        f"{FASTQ_SET_ENDPOINT}/{fastq_set_id}/linkFastq/{fastq_id}"
    )


def unlink_fastq_list_row_from_fastq_set(fastq_id: str, fastq_set_id: str) -> FastqSet:
    """
    Unlink a fastq id from a fastq set.

    :param fastq_id:
    :param fastq_set_id:
    :return:
    """

    return fastq_patch_request(
        f"{FASTQ_SET_ENDPOINT}/{fastq_set_id}/unlinkFastq/{fastq_id}"
    )


def allow_additional_fastqs_to_fastq_set(fastq_set_id: str) -> FastqSet:
    """
    Allow additional fastqs to be added to a fastq set.
    :param fastq_set_id:
    :return:
    """

    return fastq_patch_request(
        f"{FASTQ_SET_ENDPOINT}/{fastq_set_id}/allowAdditionalFastqs"
    )


def disallow_additional_fastqs_to_fastq_set(fastq_set_id: str) -> FastqSet:
    """
    Disallow additional fastqs to be added to a fastq set.
    :param fastq_set_id:
    :return:
    """

    return fastq_patch_request(
        f"{FASTQ_SET_ENDPOINT}/{fastq_set_id}/disallowAdditionalFastqs"
    )


def set_is_current_fastq_set(fastq_set_id: str) -> FastqSet:
    """
    Set a fastq set as current.
    :param fastq_set_id:
    :return:
    """
    return fastq_patch_request(
        f"{FASTQ_SET_ENDPOINT}/{fastq_set_id}/currentFastqSet"
    )


def set_is_not_current_fastq_set(fastq_set_id: str) -> FastqSet:
    """
    Set a fastq set as not current.
    :param fastq_set_id:
    :return:
    """
    return fastq_patch_request(
        f"{FASTQ_SET_ENDPOINT}/{fastq_set_id}/notCurrentFastqSet"
    )
