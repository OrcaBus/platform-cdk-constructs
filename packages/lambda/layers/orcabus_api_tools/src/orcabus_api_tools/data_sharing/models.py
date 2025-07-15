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


class PackageObject(TypedDict):
    id: str
    packageName: str
    stepsExecutionArn: str
    status: PackageStatusType
    requestTime: str
    completionTime: NotRequired[str]
    hasExpired: NotRequired[bool]


class JobPatchParameters(TypedDict):
    status: Union[PackageStatusType, PushJobStatusType]
    errorMessage: NotRequired[str]
