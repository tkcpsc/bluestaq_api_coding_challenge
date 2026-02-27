import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app import crud

"""
Tests for the CRUD (data access) layer.

These tests verify that database operations behave correctly when
creating, retrieving, listing, and deleting notes.
"""

TEST_DATABASE_URL = "sqlite:///./test_crud.db"

# Create a dedicated SQLite database for CRUD tests
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Session factory used during testing
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db():
    """
    Provide a clean database session for each test.

    The schema is recreated before each test and dropped afterward
    to ensure tests remain isolated and deterministic.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def test_create_note_persists(db):
    # Verify that a created note is persisted and can be retrieved.
    note = crud.create_note(db, "hello crud")

    assert note.id is not None
    assert note.content == "hello crud"
    assert note.created_at is not None

    # Verify the note can be retrieved from the database
    fetched = crud.get_note(db, note.id)
    assert fetched is not None
    assert fetched.id == note.id
    assert fetched.content == "hello crud"


def test_list_notes_returns_all(db):
    # Verify that listing notes returns all stored notes.
    crud.create_note(db, "a")
    crud.create_note(db, "b")

    notes = crud.list_notes(db)

    assert len(notes) == 2
    assert {n.content for n in notes} == {"a", "b"}


def test_get_note_missing_returns_none(db):
    # Verify that requesting a nonexistent note returns None.
    missing = crud.get_note(db, 123456)
    assert missing is None


def test_delete_note_returns_bool(db):
    # Verify delete behavior and return values.
    note = crud.create_note(db, "to delete")

    ok = crud.delete_note(db, note.id)
    assert ok is True

    # Ensure the note is removed
    assert crud.get_note(db, note.id) is None

    # Deleting again should return False
    ok2 = crud.delete_note(db, note.id)
    assert ok2 is False