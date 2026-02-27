from datetime import datetime
from pydantic import BaseModel, Field

"""
Pydantic schemas used for request validation and response serialization.

These models define the structure of data accepted by the API and the
format of data returned to clients.
"""


class NoteCreate(BaseModel):
    """
    Schema for creating a new note.

    Used to validate incoming request data when a client creates a note.
    """

    # Note content with basic validation constraints
    content: str = Field(min_length=1, max_length=2000)


class NoteRead(BaseModel):
    """
    Schema returned to clients when retrieving notes.

    Includes the database-generated ID and creation timestamp.
    """

    id: int
    content: str
    created_at: datetime

    # Allows Pydantic to convert SQLAlchemy objects directly into this schema
    model_config = {"from_attributes": True}