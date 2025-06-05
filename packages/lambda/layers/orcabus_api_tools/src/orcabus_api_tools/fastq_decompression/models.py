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
    TypedDict, NotRequired, Literal, List
)

JobType = Literal['FASTQ_DECOMPRESSION']
JobStatus = Literal['PENDING', 'RUNNING', 'FAILED', 'ABORTED', 'SUCCEEDED']


class JobOutput(TypedDict):
    index: str
    lane: str
    libraryId: str
    instrumentRunId: str
    read1FileUriDecompressed: str
    read2FileUriDecompressed: NotRequired[str]


class Job(TypedDict):
    id: str
    jobType: JobType
    stepsExecutionArn: str
    status: JobStatus
    startTime: str
    endTime: str
    errorMessages: NotRequired[str]
    outputs: NotRequired[List[JobOutput]]


class JobQueryParameters(TypedDict):
    fastqSetId: NotRequired[str]
    status: NotRequired[JobStatus]
    createdAfter: NotRequired[str]
    createdBefore: NotRequired[str]
    completedAfter: NotRequired[str]
    completedBefore: NotRequired[str]
    page: NotRequired[int]
    rowsPerPage: NotRequired[int]
