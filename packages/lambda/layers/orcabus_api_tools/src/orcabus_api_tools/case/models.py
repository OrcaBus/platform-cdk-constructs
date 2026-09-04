#!/usr/bin/env python3

"""TypedDict models for the case service."""

# Standard imports
from typing import TypedDict, List, Optional, Dict, NotRequired


class ExternalEntity(TypedDict):
    """An external entity linked to a case (e.g. a library, subject, or other resource)."""

    orcabusId: str
    entityType: str
    entityId: str


class Case(TypedDict):
    """A case object as returned by the case service."""

    orcabusId: str
    caseId: str
    externalEntitySet: NotRequired[List[ExternalEntity]]


class LinkEntityRequest(TypedDict):
    """Request body for linking an external entity to a case."""

    entityType: str
    entityId: str


class SyncFromRedcapRequest(TypedDict, total=False):
    """Optional request body for syncing a case from RedCap."""

    force: Optional[bool]
    fields: Optional[List[str]]
