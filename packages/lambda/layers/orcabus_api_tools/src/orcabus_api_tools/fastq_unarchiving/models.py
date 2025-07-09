#!/usr/bin/env python3

"""
{
  "id": "ufr.01JJY7P1AVFGHGVMEDE8T4VWJG",
  "jobType: "S3_UNARCHIVING",
  "stepsExecutionArn": "aws:arn:states:us-east-1:123456789012:execution:myStateMachine:myExecution",
  "status": "SUCCEEDED",
  "startTime": "2021-07-01T00:00:00Z",
  "endTime": "2021-07-01T00:00:00Z",
}
"""

from typing import (
    TypedDict, NotRequired,
    Literal
)

JobType = Literal[
    "S3_UNARCHIVING",
]


JobStatusType = Literal[
    "PENDING",
    "RUNNING",
    "FAILED",
    "ABORTED",
    "SUCCEEDED",
]

class Job(TypedDict):
    id: str
    jobType: JobType
    stepsExecutionArn: str
    status: JobStatusType
    startTime: str
    endTime: str
    errorMessages: str


class JobQueryParameters(TypedDict):
    fastqId: NotRequired[str]
    status: NotRequired[JobStatusType]
    createdAfter: NotRequired[str]
    createdBefore: NotRequired[str]
    completedAfter: NotRequired[str]
    completedBefore: NotRequired[str]
    page: NotRequired[int]
    rowsPerPage: NotRequired[int]