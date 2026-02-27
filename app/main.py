from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .db import Base, engine, SessionLocal
from . import crud, schemas

"""
Main FastAPI application for the Notes Vault API.

This module defines the HTTP routes that expose the application's
functionality. Routes delegate database operations to the CRUD layer
and use schema models to validate input and format responses.
"""

# Create database tables on application startup (simple approach for MVP)
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Notes Vault API",
    version="1.0.0",
    description="MVP Notes API: create, list, fetch, and delete notes.",
)


def get_db():
    """
    Dependency that provides a database session to each request.

    A new SQLAlchemy session is created when a request starts and
    closed after the request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def not_found(note_id: int) -> HTTPException:
    """
    Helper function to generate a standardized 404 error response.

    Args:
        note_id: ID of the note that was requested.

    Returns:
        HTTPException configured with a consistent error structure.
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"error": "not_found", "message": f"Note {note_id} does not exist"},
    )


@app.post("/notes", response_model=schemas.NoteRead, status_code=status.HTTP_201_CREATED)
def create_note(payload: schemas.NoteCreate, db: Session = Depends(get_db)):
    """
    Create a new note.

    Args:
        payload: Request body containing note content.
        db: Database session provided by dependency injection.

    Returns:
        The newly created note.
    """
    return crud.create_note(db, content=payload.content)


@app.get("/notes", response_model=list[schemas.NoteRead], status_code=status.HTTP_200_OK)
def list_notes(db: Session = Depends(get_db)):
    """
    Retrieve all notes.

    Args:
        db: Database session.

    Returns:
        A list of notes ordered by creation time (newest first).
    """
    return crud.list_notes(db)


@app.get("/notes/{id}", response_model=schemas.NoteRead, status_code=status.HTTP_200_OK)
def get_note(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single note by ID.

    Args:
        id: Note identifier.
        db: Database session.

    Returns:
        The requested note.

    Raises:
        HTTPException: If the note does not exist.
    """
    note = crud.get_note(db, id)
    if note is None:
        raise not_found(id)
    return note


@app.delete("/notes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(id: int, db: Session = Depends(get_db)):
    """
    Delete a note by ID.

    Args:
        id: Note identifier.
        db: Database session.

    Raises:
        HTTPException: If the note does not exist.
    """
    ok = crud.delete_note(db, id)
    if not ok:
        raise not_found(id)
    return None