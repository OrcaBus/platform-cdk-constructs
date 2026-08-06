#!/usr/bin/env python3

"""TypedDict models for the data sharing service."""

from typing import Literal, TypedDict, NotRequired, Union

PackageStatusType = Literal[
    "PENDING",
    "RUNNING",
    "FAILED",
    "ABORTED",
    "SUCCEEDED",
]

PushJobStatusType = Literal[
    "PENDING",
    "RUNNING",
    "FAILED",
    "ABORTED",
    "SUCCEEDED",
]


class PackageObjectDict(TypedDict):
    """Data sharing package object with status and metadata."""

    id: str
    packageName: str
    stepsExecutionArn: str
    status: PackageStatusType
    requestTime: str
    completionTime: NotRequired[str]
    hasExpired: NotRequired[bool]


class PushJobObjectDict(TypedDict):
    """Push job object representing a data sharing transfer."""

    id: str
    stepFunctionsExecutionArn: str
    status: PushJobStatusType
    startTime: str
    packageId: str
    shareDestination: str
    logUri: NotRequired[str]
    endTime: NotRequired[str]
    errorMessages: NotRequired[str]


class JobPatchParameters(TypedDict):
    """Parameters for updating a package or push job status."""

    status: Union[PackageStatusType, PushJobStatusType]
    errorMessage: NotRequired[str]
