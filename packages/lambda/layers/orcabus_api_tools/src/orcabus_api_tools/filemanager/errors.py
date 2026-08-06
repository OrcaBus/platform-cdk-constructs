"""Custom exception classes for the File Manager service."""

# Imports
from typing import Optional


class S3FileNotFoundError(Exception):
    """Raised when a file cannot be found in the File Manager by ID, URI, or ingest ID."""

    def __init__(
            self,
            s3_object_id: Optional[str] = None,
            s3_uri: Optional[str] = None,
            ingest_id: Optional[str] = None
    ):
        self.s3_object_id = s3_object_id
        self.s3_uri = s3_uri
        self.ingest_id = ingest_id
        if s3_object_id is not None:
            self.message = f"Could not find file with object ID '{s3_object_id}'"
        elif s3_uri is not None:
            self.message = f"Could not find the file at S3 URI '{s3_uri}'"
        elif ingest_id is not None:
            self.message = f"Could not find file with ingest ID '{ingest_id}'"
        else:
            self.message = "Could not find file"
        super().__init__(self.message)


class S3DuplicateFileCopyError(Exception):
    """Raised when multiple file copies are found for the same identifier."""

    def __init__(
            self,
            s3_object_id: Optional[str] = None,
            s3_uri: Optional[str] = None,
            ingest_id: Optional[str] = None
    ):
        self.s3_object_id = s3_object_id
        self.s3_uri = s3_uri
        self.ingest_id = ingest_id
        if s3_object_id is not None:
            self.message = f"Found multiple files with the object ID '{s3_object_id}'"
        elif s3_uri is not None:
            self.message = f"Found multiple files with the uri'{s3_uri}'"
        elif ingest_id is not None:
            self.message = f"Found multiple files with the ingest id '{ingest_id}'"
        else:
            self.message = "Found multiple files"
        super().__init__(self.message)

