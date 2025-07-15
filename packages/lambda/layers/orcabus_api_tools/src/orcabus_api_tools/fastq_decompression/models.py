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
    TypedDict, NotRequired, Literal, List, Union
)

JobType = Literal['FASTQ_DECOMPRESSION']
JobStatusType = Literal['PENDING', 'RUNNING', 'FAILED', 'ABORTED', 'SUCCEEDED']

# Output jobs
class DecompressionJobOutputObjectItem(TypedDict):
    ingestId: str
    gzipFileUri: str


class DecompressionJobOutputObjectFastqId(TypedDict):
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


class DecompressionJobOutputObject(TypedDict):
   # Decompressed file URI by ORA file ingest ID list
   decompressedFileList: List[DecompressionJobOutputObjectFastqId]

class GzipFileSizeCalculationOutputObject(TypedDict):
    # Gzip file size by ORA file ingest ID list
    gzipFileSizeList: List[GzipFileSizeCalculationOutputsFastqId]


class RawMd5sumCalculationOutputObject(TypedDict):
    # Raw md5sum by ORA file ingest ID list
    rawMd5sumList: List[RawMd5sumCalculationOutputsFastqId]


JobOutputType = Union[
  DecompressionJobOutputObject |
  GzipFileSizeCalculationOutputObject |
  RawMd5sumCalculationOutputObject
]

class Job(TypedDict):
    id: str
    jobType: JobType
    stepsExecutionArn: str
    status: JobStatusType
    startTime: str
    endTime: str
    errorMessages: NotRequired[str]
    outputs: NotRequired[JobOutputType]


class JobCreateParameters(TypedDict):
    fastqIdList: List[str]
    jobType: JobType
    maxReads: NotRequired[int]
    outputUriPrefix: NotRequired[str]
    sampling: NotRequired[bool]


class JobQueryParameters(TypedDict):
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
    status: JobStatusType
    errorMessage: NotRequired[str]
    stepsExecutionArn: NotRequired[str]
    output: NotRequired[JobOutputType]
