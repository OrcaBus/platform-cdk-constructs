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
from .globals import FASTQ_ENDPOINT, FASTQ_SET_ENDPOINT
from .models import (
    QcStats, Fastq, ReadCount,
    FileCompressionInformation, FileStorageObject, ReadSet,
    FastqSet
)


def add_qc_stats(fastq_id: str, qc_stats: QcStats) -> Fastq:
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
        f"{FASTQ_ENDPOINT}/{fastq_id}/addQcStats",
        json_data=dict(qc_stats)
    )


def add_read_count(fastq_id: str, read_count: ReadCount) -> Fastq:
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
        f"{FASTQ_ENDPOINT}/{fastq_id}/addReadCount",
        json_data=dict(read_count)
    )


def add_file_compression_information(fastq_id: str, file_compression_information: FileCompressionInformation) -> Fastq:
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
        f"{FASTQ_ENDPOINT}/{fastq_id}/addFileCompressionInformation",
        json_data=dict(file_compression_information)
    )


def add_ntsm_storage_object(fastq_id: str, ntsm_fastq_storage_object: FileStorageObject) -> Fastq:
    """
    Add a Ntsm storage object to a fastq id.

    :param fastq_id: Fastq str
    :param ntsm_fastq_storage_object: Ntsm str
    """
    for key in ntsm_fastq_storage_object.keys():
        if key not in FileStorageObject.__annotations__:
            raise ValueError(f"Invalid parameter: {key}")

    return fastq_patch_request(
        f"{FASTQ_ENDPOINT}/{fastq_id}/addNtsmStorageObject",
        json_data=dict(ntsm_fastq_storage_object)
    )


def add_read_set(fastq_id: str, read_set: ReadSet) -> Fastq:
    """
    Add a read set to a fastq id.

    :param fastq_id: Fastq str
    :param read_set: ReadSet str
    """
    for key in read_set.keys():
        if key not in ReadSet.__annotations__:
            raise ValueError(f"Invalid parameter: {key}")

    return fastq_patch_request(
        f"{FASTQ_ENDPOINT}/{fastq_id}/addFastqPairStorageObject",
        json_data=dict(read_set)
    )


def detach_read_set(fastq_id: str) -> Fastq:
    """
    Detach a read set to a fastq id.

    :param fastq_id: Fastq str
    """
    return fastq_patch_request(
        f"{FASTQ_ENDPOINT}/{fastq_id}/detachFastqPairStorageObject"
    )


def validate_fastq(fastq_id: str) -> Fastq:
    """
    Validate a fastq id.

    :param fastq_id: Fastq str
    """
    return fastq_patch_request(
        f"{FASTQ_ENDPOINT}/{fastq_id}/validate"
    )


def invalidate_fastq(fastq_id: str) -> Fastq:
    """
    Invalidate a fastq id.

    :param fastq_id: Fastq str
    """
    return fastq_patch_request(
        f"{FASTQ_ENDPOINT}/{fastq_id}/invalidate"
    )


def link_fastq_list_row_to_fastq_set(fastq_id: str, fastq_set_id: str) -> FastqSet:
    """
    Deprecated: Use `link_fastq_to_fast_set` instead.
    Link a fastq id to a fastq set.

    :param fastq_id:
    :param fastq_set_id:
    :return:
    """
    return link_fastq_to_fastq_set(
        fastq_id=fastq_id,
        fastq_set_id=fastq_set_id
    )


def link_fastq_to_fastq_set(fastq_id: str, fastq_set_id: str) -> FastqSet:
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
    Deprecated: Use `unlink_fastq_from_fastq_set` instead.
    """
    return unlink_fastq_from_fastq_set(
        fastq_id=fastq_id,
        fastq_set_id=fastq_set_id
    )


def unlink_fastq_from_fastq_set(fastq_id: str, fastq_set_id: str) -> FastqSet:
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
