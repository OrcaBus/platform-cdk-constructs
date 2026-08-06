#!/usr/bin/env python3

"""
{
  "id": "ufr.01JJY7P1AVFGHGVMEDE8T4VWJG",
  "jobType: "FASTQ_DECOMPRESSION",
  "stepsExecutionArn": "aws:arn:states:us-east-1:123456789012:execution:myStateMachine:myExecution",
  "status": "SUCCEEDED",
  "startTime": "2021-07-01T00:00:00Z",
  "endTime": "2021-07-01T00:00:00Z",
}
"""

from typing import (
    TypedDict, NotRequired, Literal, List, Union, Dict
)

JobType = Literal['FASTQ_DECOMPRESSION']
JobStatusType = Literal['PENDING', 'RUNNING', 'FAILED', 'ABORTED', 'SUCCEEDED']

# Output jobs
class DecompressionJobOutputObjectItem(TypedDict):
    """Single decompressed file output item mapping an ingest ID to its GZIP file URI."""
    ingestId: str
    gzipFileUri: str


class DecompressionJobOutputObjectFastqId(TypedDict):
    """Decompression output for a single FASTQ, containing its decompressed file URIs."""
    fastqId: str
    decompressedFileUriByOraFileIngestIdList: List[DecompressionJobOutputObjectItem]


class GzipFileSizeCalculationOutputObjectItem(TypedDict):
    ingestId: str
    gzipFileSize: int


class GzipFileSizeCalculationOutputsFastqId(TypedDict):
    fastqId: str
    gzipFileSizeByOraFileIngestIdList: List[GzipFileSizeCalculationOutputObjectItem]


class RawMd5sumCalculationOutputsObjectItem(TypedDict):
    ingestId: str
    rawMd5sum: str


class RawMd5sumCalculationOutputsFastqId(TypedDict):
    fastqId: str
    rawMd5sumByOraFileIngestIdList: List[RawMd5sumCalculationOutputsObjectItem]


class ReadCountCalculationOutputsFastqId(TypedDict):
    fastqId: str
    readCount: int


class DecompressionJobOutputObject(TypedDict):
   # Decompressed file URI by ORA file ingest ID list
   decompressedFileList: List[DecompressionJobOutputObjectFastqId]


class GzipFileSizeCalculationOutputObject(TypedDict):
    # Gzip file size by ORA file ingest ID list
    gzipFileSizeList: List[GzipFileSizeCalculationOutputsFastqId]


class RawMd5sumCalculationOutputObject(TypedDict):
    # Raw md5sum by ORA file ingest ID list
    rawMd5sumList: List[RawMd5sumCalculationOutputsFastqId]


class ReadCountCalculationOutputObject(TypedDict):
    # Raw md5sum by ORA file ingest ID list
    readCountList: List[ReadCountCalculationOutputsFastqId]


JobOutputType = Union[
  DecompressionJobOutputObject |
  GzipFileSizeCalculationOutputObject |
  RawMd5sumCalculationOutputObject |
  ReadCountCalculationOutputObject
]

class Job(TypedDict):
    """Decompression job object representing the state of a decompression task."""
    id: str
    jobType: JobType
    stepsExecutionArn: str
    status: JobStatusType
    startTime: str
    endTime: str
    errorMessages: NotRequired[str]
    outputs: NotRequired[JobOutputType]


class JobCreateParameters(TypedDict):
    """Parameters for creating a new decompression job."""
    fastqIdList: List[str]
    jobType: JobType
    maxReads: NotRequired[int]
    outputUriPrefix: NotRequired[str]
    sampling: NotRequired[bool]
    noSplitByLane: NotRequired[bool]
    fileUriByFastqIdMap: NotRequired[Dict[str, List[str]]]


class JobQueryParameters(TypedDict):
    """Query parameters for filtering decompression jobs."""
    fastqId: NotRequired[str]
    fastqSetId: NotRequired[str]
    status: NotRequired[JobStatusType]
    createdAfter: NotRequired[str]
    createdBefore: NotRequired[str]
    completedAfter: NotRequired[str]
    completedBefore: NotRequired[str]
    page: NotRequired[int]
    rowsPerPage: NotRequired[int]


class JobUpdateParameters(TypedDict):
    """Parameters for updating a decompression job's status."""
    status: JobStatusType
    errorMessage: NotRequired[str]
    stepsExecutionArn: NotRequired[str]
    output: NotRequired[JobOutputType]
