"""TypedDict models for the ICAv2 WES (Workflow Execution Service)."""

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
    """Engine parameters for ICAv2 pipeline execution."""

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
    """Parameters for updating a WES analysis status."""

    status: str
    icav2AnalysisId: NotRequired[str]
    errorType: NotRequired[str]
    errorMessageUri: NotRequired[str]
    stepsLaunchExecutionArn: NotRequired[str]


class WESResponse(TypedDict):
    """WES analysis response object with status and metadata."""

    id: str
    name: str
    state: str
    inputs: Dict[str, Any]
    outputs: NotRequired[Dict[str, Any]]
    engineParameters: EngineParameters
    tags: NotRequired[Dict[str, Any]]
    icav2AnalysisId: NotRequired[str]
    createdAt: str
    updatedAt: str
    projectId: str
    pipelineId: str
    status: str
    errorMessage: str
