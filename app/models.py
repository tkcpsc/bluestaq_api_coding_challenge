from datetime import datetime, timezone
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

"""
Database models for the Notes API.

This module defines the SQLAlchemy ORM models that map Python classes
to database tables.
"""


class Note(Base):
    """
    ORM model representing a note stored in the database.

    Each note contains text content and a timestamp indicating when it
    was created.
    """

    __tablename__ = "notes"

    # Unique identifier for the note
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Text content of the note
    content: Mapped[str] = mapped_column(String, nullable=False)

    # Timestamp automatically set when the note is created
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )