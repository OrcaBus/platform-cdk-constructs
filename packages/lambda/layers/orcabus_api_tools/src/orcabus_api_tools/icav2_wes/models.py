from typing import (
    TypedDict, Dict, Any, Literal, NotRequired
)

AnalysisStorageSize = Literal['SMALL', 'MEDIUM', 'LARGE']
STATUS = Literal[
    'SUBMITTED',
    'PENDING',
    'RUNNABLE',
    'STARTING',
    'RUNNING',
    'SUCCEEDED',
    'FAILED',
    'ABORTED',
]


class EngineParameters(TypedDict):
    # Launch Configurations
    pipelineId: str
    projectId: str
    analysisStorageSize: AnalysisStorageSize
    # Locations
    outputUri: str
    logsUri: str
    cacheUri: NotRequired[str]


class WESPostRequest(TypedDict):
    """WES request object."""
    name: str
    inputs: Dict[str, Any]
    engineParameters: EngineParameters
    tags: NotRequired[Dict[str, Any]]


class WESPatchRequest(TypedDict):
    status: str
    icav2AnalysisId: NotRequired[str]


class WESResponse(TypedDict):
    """WES response object."""
    id: str
    name: str
    state: str
    inputs: Dict[str, Any]
    outputs: NotRequired[Dict[str, Any]]
    engineParameters: EngineParameters
    tags: NotRequired[Dict[str, Any]]
    createdAt: str
    updatedAt: str
    projectId: str
    pipelineId: str
    status: str
    errorMessage: str
