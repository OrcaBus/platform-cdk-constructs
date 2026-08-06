#!/usr/bin/env python3

"""
TypedDict models

Workflow Run is (when the workflow is queried directly
{
  "orcabusId": "wfr.01JDTT7CEYQ0K2E6MCRB9GKX3T",
  "currentState": {
    "orcabusId": "stt.01JE15KJ57R24SEPZZ710MDMDM",
    "status": "SUCCEEDED",
    "timestamp": "2024-12-01T13:12:22.071000Z"
  },
  "libraries": [
    {
      "orcabusId": "lib.01JBMTM4SYY7QH03HM6XF6X0TT",
      "libraryId": "L2000696"
    },
    ...
  ],
  "workflow": {
    "orcabusId": "wfl.01JD7C2HWVR5KF7VWWQPH0M0FZ",
    "name": "ora-compression",
    "version": "4-2-4--v2",
    "executionEngine": "Unknown",
    "executionEnginePipelineId": "Unknown"
  },
  "analysisRun": null,
  "portalRunId": "20241122b2e1f778",
  "executionId": null,
  "workflowRunName": "umccr--automated--ora-compression--4-2-4--v2--20241122b2e1f778",
  "comment": null
}

When the workflow is queried from the workflow run list


State is

Payload is
"""

# Imports
from typing import TypedDict, Optional, Dict, List, NotRequired, Literal

# Import directly, safe as we do not do any internal imports under metadata.models.
from ..metadata.models import LibraryBase

# Literals
AnalysisStatusType = Literal[
    'ACTIVE',
    'INACTIVE',
]
ContextUseCaseType = Literal[
    'COMPUTE',
    'STORAGE',
]

ExecutionEngineType = Literal[
    'Unknown',
    'ICA',
    'SEQERA',
    'AWS_BATCH',
    'AWS_ECS',
    'AWS_EKS',
]

ValidationStateType = Literal[
    'UNVALIDATED',
    'VALIDATED',
    'DEPRECATED',
    'FAILED',
]

# Classes
class StateDetail(TypedDict):
    """Brief workflow run state with status and timestamp."""

    orcabusId: str
    status: str
    timestamp: str


class State(StateDetail):
    """Full workflow run state including comment and references."""

    comment: str
    workflowRun: str
    payload: str


class Analysis(TypedDict):
    """Analysis definition with name, version, and status."""

    orcabusId: str
    analysisName: str
    analysisVersion: str
    status: AnalysisStatusType


class Context(TypedDict):
    """Execution context specifying compute or storage resources."""

    orcabusId: str
    name: str
    usecase: ContextUseCaseType


class AnalysisRun(TypedDict):
    """An analysis run instance linking an analysis to contexts and readsets."""

    orcabusId: str
    analysis: Analysis
    storageContext: Context
    computeContext: Context
    analysisRunName: str
    comment: NotRequired[str]
    contexts: List[str]
    readsets: List[str]


class Workflow(TypedDict):
    """Workflow definition with name, version, and execution engine details."""

    orcabusId: str
    name: str
    version: str
    codeVersion: NotRequired[str]
    executionEngine: NotRequired[str]
    executionEnginePipelineId: NotRequired[str]
    validationState: NotRequired[str]


class ReadSet(TypedDict):
    """A read set reference with OrcaBus ID and RGID."""

    orcabusId: str
    rgid: str


class EventLibrary(LibraryBase):
    """Library object with associated readsets for event processing."""

    readsets: List[ReadSet]


class WorkflowRunDetail(TypedDict):
    """Detailed workflow run object without library information."""

    orcabusId: str
    currentState: StateDetail
    workflow: Workflow
    portalRunId: str
    executionId: Optional[str]
    workflowRunName: str
    comment: Optional[str]
    analysisRun: Optional[AnalysisRun]
    contexts: NotRequired[List[str]]
    readsets: NotRequired[List[str]]


class WorkflowRun(WorkflowRunDetail):
    """Full workflow run object including associated libraries."""

    libraries: List[Dict[str, str]]


class Payload(TypedDict):
    """Workflow run payload containing versioned data."""

    orcabusId: str
    payloadRefId: str
    version: str
    data: Dict