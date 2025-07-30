#!/usr/bin/env python3

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
    id: str
    packageName: str
    stepsExecutionArn: str
    status: PackageStatusType
    requestTime: str
    completionTime: NotRequired[str]
    hasExpired: NotRequired[bool]


class PushJobObjectDict(TypedDict):
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
    status: Union[PackageStatusType, PushJobStatusType]
    errorMessage: NotRequired[str]
