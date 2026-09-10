#!/usr/bin/env python3

"""TypedDict models for the case service.

Generated to match the Case Manager API schema
(https://case.prod.umccr.org/schema/openapi.json).

Notes:
- ``readOnly`` schema fields are always present in server responses, so they are
  modelled as required keys.
- ``nullable`` schema fields are modelled with ``Optional[...]`` (i.e. the value
  may be ``None``).
- Fields that are optional in the payload (not in the schema ``required`` list)
  are modelled with ``NotRequired[...]``.
- ``*Request`` models describe request bodies and use ``NotRequired`` for
  writable-but-optional fields.
"""

# Standard imports
from typing import TypedDict, List, Dict, Optional, NotRequired, Literal, Any


# Enums
StatusType = Literal[
    'request_received',
    'wgts_tumour_sample_received',
    'wgts_germline_sample_received',
    'cttso_sample_received',
    'all_sample_received',
    'library_partially_failed',
    'sequencing_started',
    'sequencing_completed',
    'bioinformatics_started',
    'bioinformatics_completed',
    'curation_started',
    'curation_completed',
    'locked',
    'unlocked',
    'failed',
    'completed',
    'archived',
]

StudyType = Literal[
    'clinical',
    'research',
]

CaseType = Literal[
    'wgts',
    'cttso',
    'wgs_n',
]

ExternalServiceType = Literal[
    'redcap',
]


# Comment
class Comment(TypedDict):
    """A comment attached to a case or a state."""

    orcabusId: str
    createdBy: Optional[str]
    archivedBy: Optional[str]
    text: NotRequired[Optional[str]]
    createdAt: str
    isArchived: NotRequired[bool]
    archivedAt: Optional[str]
    case: NotRequired[Optional[str]]
    state: NotRequired[Optional[str]]


class CommentRequest(TypedDict):
    """Request body for creating a comment."""

    text: NotRequired[Optional[str]]
    isArchived: NotRequired[bool]
    case: NotRequired[Optional[str]]
    state: NotRequired[Optional[str]]


class PatchedCommentRequest(TypedDict):
    """Request body for partially updating a comment."""

    text: NotRequired[Optional[str]]
    isArchived: NotRequired[bool]
    case: NotRequired[Optional[str]]
    state: NotRequired[Optional[str]]


# State
class State(TypedDict):
    """A case state (status transition)."""

    orcabusId: str
    createdBy: Optional[str]
    archivedBy: Optional[str]
    status: StatusType
    eventDate: NotRequired[str]
    eventTime: NotRequired[Optional[str]]
    createdAt: str
    isArchived: bool
    archivedAt: Optional[str]
    case: str


class StateDetail(TypedDict):
    """A case state including its associated comment.

    ``comment`` is documented as required in the schema but is omitted by the
    list endpoint when the state has no associated comment, so it is modelled as
    ``NotRequired``.
    """

    orcabusId: str
    comment: NotRequired[Optional[Comment]]
    createdBy: Optional[str]
    archivedBy: Optional[str]
    status: StatusType
    eventDate: NotRequired[str]
    eventTime: NotRequired[Optional[str]]
    createdAt: str
    isArchived: bool
    archivedAt: Optional[str]
    case: str


class StateDetailRequest(TypedDict):
    """Request body for creating a state."""

    status: StatusType
    eventDate: NotRequired[str]
    eventTime: NotRequired[Optional[str]]
    case: str


class PatchedStateDetailRequest(TypedDict):
    """Request body for partially updating a state."""

    status: NotRequired[StatusType]
    eventDate: NotRequired[str]
    eventTime: NotRequired[Optional[str]]
    case: NotRequired[str]


# User
class User(TypedDict):
    """A user record."""

    orcabusId: str
    email: str
    name: NotRequired[Optional[str]]


class UserRequest(TypedDict):
    """Request body describing a user."""

    email: str
    name: NotRequired[Optional[str]]


# External entity
class ExternalEntity(TypedDict):
    """An external entity (e.g. a library) that can be linked to a case."""

    orcabusId: str
    prefix: NotRequired[Optional[str]]
    type: NotRequired[Optional[str]]
    serviceName: NotRequired[Optional[str]]
    alias: NotRequired[Optional[str]]


class ExternalEntityRequest(TypedDict):
    """Request body describing an external entity."""

    prefix: NotRequired[Optional[str]]
    type: NotRequired[Optional[str]]
    serviceName: NotRequired[Optional[str]]
    alias: NotRequired[Optional[str]]


class PendingExternalEntity(TypedDict):
    """An external entity referenced by a case but not yet resolved/created."""

    orcabusId: str
    alias: NotRequired[Optional[str]]
    type: NotRequired[Optional[str]]
    serviceName: NotRequired[Optional[str]]


class PendingExternalEntityRequest(TypedDict):
    """Request body describing a pending external entity."""

    alias: NotRequired[Optional[str]]
    type: NotRequired[Optional[str]]
    serviceName: NotRequired[Optional[str]]


# Case (summary / base form)
class CaseBase(TypedDict):
    """A case as returned by the case service (summary form).

    This is the primitive/summary representation embedded when a case is
    referenced from another resource (e.g. a user or external entity). Most
    descriptive fields are REDCap-managed and returned read-only.
    """

    orcabusId: str
    alias: NotRequired[List[str]]
    rnasumReferences: NotRequired[List[str]]
    requestFormId: str
    type: CaseType
    studyName: Optional[str]
    studyId: Optional[str]
    urNumber: Optional[str]
    description: NotRequired[Optional[str]]
    studyType: StudyType
    isReportRequired: NotRequired[bool]
    isNataAccredited: NotRequired[bool]
    links: NotRequired[Optional[Dict[str, str]]]
    redcapPayload: Optional[Dict[str, Any]]
    dueDate: NotRequired[Optional[str]]


# Link objects (reference CaseBase / ExternalEntity / User defined above)
class UserCase(TypedDict):
    """A case linked to a user, with link metadata."""

    description: NotRequired[Optional[str]]
    timestamp: str
    case: CaseBase


class UserDetail(TypedDict):
    """A user including the set of cases they are linked to."""

    orcabusId: NotRequired[str]
    caseSet: List[UserCase]
    email: str
    name: NotRequired[Optional[str]]


class ExternalEntityCaseLink(TypedDict):
    """A case linked to an external entity, with link metadata."""

    timestamp: str
    case: CaseBase


class ExternalEntityDetail(TypedDict):
    """An external entity including the set of cases it is linked to."""

    orcabusId: NotRequired[str]
    case: List[ExternalEntityCaseLink]
    prefix: NotRequired[Optional[str]]
    type: NotRequired[Optional[str]]
    serviceName: NotRequired[Optional[str]]
    alias: NotRequired[Optional[str]]


class CaseExternalEntityLink(TypedDict):
    """An external entity linked to a case, with link metadata."""

    timestamp: str
    externalEntity: ExternalEntity


class CaseExternalEntityLinkCreate(TypedDict):
    """Response body for linking an external entity to a case."""

    id: int
    case: str
    externalEntity: str
    timestamp: str


class CaseExternalEntityLinkCreateRequest(TypedDict):
    """Request body for linking an external entity to a case."""

    externalEntity: str


class CaseUserLink(TypedDict):
    """A user linked to a case, with link metadata."""

    description: NotRequired[Optional[str]]
    timestamp: str
    user: User


class CaseUserLinkRequest(TypedDict):
    """Request body describing a case-user link."""

    description: NotRequired[Optional[str]]


class CaseUserCreate(TypedDict):
    """Response body for linking a user to a case."""

    id: int
    case: str
    user: str
    description: NotRequired[Optional[str]]
    timestamp: str


class CaseUserCreateRequest(TypedDict):
    """Request body for linking a user (by email) to a case."""

    email: str
    description: NotRequired[Optional[str]]


# Case (detailed form, with related sets)
class CaseDetail(CaseBase):
    """A case with its related sets (external entities, users, states, comments).

    Extends :class:`CaseBase` with the linked collections that the case service
    embeds inline. This is the shape returned by both the list and retrieve
    endpoints.
    """

    externalEntitySet: List[CaseExternalEntityLink]
    pendingExternalEntities: List[PendingExternalEntity]
    userSet: List[CaseUserLink]
    latestState: Optional[State]
    commentSet: List[Comment]


class PatchedCaseDetailRequest(TypedDict):
    """Request body for partially updating a case (writable fields only)."""

    alias: NotRequired[List[str]]
    rnasumReferences: NotRequired[List[str]]
    description: NotRequired[Optional[str]]
    studyType: NotRequired[StudyType]
    isReportRequired: NotRequired[bool]
    isNataAccredited: NotRequired[bool]
    links: NotRequired[Optional[Dict[str, str]]]
    dueDate: NotRequired[Optional[str]]


# Timeline / activity
class CaseTimeline(TypedDict):
    """A single entry in a case's activity timeline."""

    timestamp: str
    eventType: str
    modelType: str
    actor: Optional[str]
    description: str
    detail: Optional[Dict[str, Any]]


# Sync / external service
class ExternalSyncLog(TypedDict):
    """A record of a sync from an external service (e.g. REDCap)."""

    id: int
    externalService: ExternalServiceType
    importedAt: str


class RedcapDateRangeSyncRequest(TypedDict):
    """Request body for syncing cases from REDCap over a date range."""

    afterDate: str
    beforeDate: NotRequired[Optional[str]]
