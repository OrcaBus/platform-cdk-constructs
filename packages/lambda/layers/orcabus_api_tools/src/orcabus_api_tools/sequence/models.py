#!/usr/bin/env python3

"""TypedDict models for the sequence service."""

# Standard imports
from typing import TypedDict, Literal, Optional, Dict, List

# Type hints
StatusType = Literal['STARTED', 'FAILED', 'SUCCEEDED', 'ABORTED', 'RESOLVED']


class SequenceDetail(TypedDict):
    """Sequence detail object with instrument run metadata."""

    orcabusId: str
    instrumentRunId: str
    experimentName: str
    startTime: str
    endTime: Optional[str]
    status: Optional[StatusType]


class Sequence(TypedDict):
    """Full sequence object with all run metadata and associated libraries."""

    orcabusId: str
    libraries: List[str]
    sequenceRunId: str
    status: StatusType
    startTime: str
    sampleSheetName: str
    v1pre3Id: str
    icaProjectId: str
    apiUrl: str
    endTime: str
    runVolumeName: str
    runFolderPath: str
    runDataUri: str
    instrumentRunId: str
    reagentBarcode: str
    flowcellBarcode: str
    sequenceRunName: str
    experimentName: str


class SampleSheet(TypedDict):
    """Sample sheet object associated with a sequence run."""

    orcabusId: str
    sampleSheetName: str
    associationStatus: str
    associationTimestamp: str
    sampleSheetContent: Optional[Dict]
    sequence: str