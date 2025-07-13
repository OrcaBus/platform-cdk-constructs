from typing import Literal, TypedDict, NotRequired

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


class PackageObject(TypedDict):
    id: str
    packageName: str
    stepsExecutionArn: str
    status: PackageStatusType
    requestTime: str
    completionTime: NotRequired[str]
    hasExpired: NotRequired[bool]


class JobPatchParameters(TypedDict):
    status: str
    errorMessage: NotRequired[str]
