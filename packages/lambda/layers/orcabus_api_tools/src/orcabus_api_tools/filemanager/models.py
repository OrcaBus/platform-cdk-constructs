from typing import (
    Optional,
    TypedDict,
    Dict,
    Literal,
    NotRequired,
    Any
)

"""
Example File Object response
    {
      "attributes": null,
      "bucket": "string",
      "deletedDate": "2025-01-19T23:32:42.747Z",
      "deletedSequencer": "string",
      "eTag": "string",
      "eventTime": "2025-01-19T23:32:42.747Z",
      "eventType": "Created",
      "ingestId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "isCurrentState": true,
      "isDeleteMarker": true,
      "key": "string",
      "lastModifiedDate": "2025-01-19T23:32:42.747Z",
      "numberDuplicateEvents": 9007199254740991,
      "numberReordered": 9007199254740991,
      "s3ObjectId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "sequencer": "string",
      "sha256": "string",
      "size": 9007199254740991,
      "storageClass": null,
      "versionId": "string"
    }
"""

StorageClassType = Literal[
    "Standard",
    "StandardIa",
    "IntelligentTiering",
    "GlacierIr",
    "Glacier",
    "DeepArchive",
]

StorageClassPriority: Dict[StorageClassType, int] = {
    "Standard": 1,
    "StandardIa": 2,
    "IntelligentTiering": 3,
    "GlacierIr": 4,
    "Glacier": 5,
    "DeepArchive": 6,
}

EventType = Literal[
    "Created",
    "Deleted",
    "Other"
]

ReasonType = Literal[
    "CreatedPut",
    "CreatedPost",
    "CreatedCopy",
    "CreatedCompleteMultipartUpload",
    "Deleted",
    "DeletedLifecycle",
    "Restored",
    "RestoreExpired",
    "StorageClassChanged",
    "Crawl",
    "Unknown",
    "CrawlRestored"
]

ArchiveStatusType = Literal[
    "ArchiveAccess",
    "DeepArchiveAccess"
]


class FileQueryParameters(TypedDict):
    caseSensitive: NotRequired[bool]
    currentState: NotRequired[bool]
    eventType: NotRequired[EventType]
    bucket: NotRequired[str]
    key: NotRequired[str]
    versionId: NotRequired[str]
    eventTime: NotRequired[str]
    size: NotRequired[int]
    sha256: NotRequired[str]
    lastModifiedDate: NotRequired[str]
    eTag: NotRequired[str]
    storageClass: NotRequired[StorageClassType]
    isDeleteMarker: NotRequired[bool]
    reason: NotRequired[ReasonType]
    archiveStatus: NotRequired[ArchiveStatusType]
    isAccessible: NotRequired[bool]
    ingestId: NotRequired[str]
    attributes: NotRequired[Dict[str, Any]]


class FileObject(TypedDict):
    # Identifier
    s3ObjectId: str

    # Path attributes
    bucket: str
    key: str

    # File attributes
    eTag: str
    eventTime: str
    eventType: str
    ingestId: str
    isCurrentState: bool
    isDeleteMarker: bool
    lastModifiedDate: str
    numberDuplicateEvents: int
    numberReordered: int
    sequencer: str
    size: int
    storageClass: StorageClassType

    # Attribute attributes
    attributes: Optional[Dict]

    # Optional attributes
    deletedDate: Optional[str]
    deletedSequencer: Optional[str]
    versionId: Optional[str]
    sha256: Optional[str]