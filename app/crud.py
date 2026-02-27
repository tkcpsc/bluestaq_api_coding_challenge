from sqlalchemy.orm import Session
from .models import Note


def create_note(db: Session, content: str) -> Note:
    """
    Create and persist a new note in the database.

    Args:
        db: Active SQLAlchemy database session.
        content: Text content of the note.

    Returns:
        The newly created Note object with generated id and created_at fields.
    """
    note = Note(content=content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def list_notes(db: Session) -> list[Note]:
    """
    Retrieve all notes from the database.

    Notes are returned in descending order by creation time so that the
    most recently created notes appear first.

    Args:
        db: Active SQLAlchemy database session.

    Returns:
        A list of Note objects.
    """
    return db.query(Note).order_by(Note.created_at.desc()).all()


def get_note(db: Session, note_id: int) -> Note | None:
    """
    Fetch a single note by its ID.

    Args:
        db: Active SQLAlchemy database session.
        note_id: ID of the note to retrieve.

    Returns:
        The Note object if found, otherwise None.
    """
    return db.get(Note, note_id)


def delete_note(db: Session, note_id: int) -> bool:
    """
    Delete a note by its ID.

    Args:
        db: Active SQLAlchemy database session.
        note_id: ID of the note to delete.

    Returns:
        True if the note was successfully deleted,
        False if the note does not exist.
    """
    note = db.get(Note, note_id)
    if note is None:
        return False
    db.delete(note)
    db.commit()
    return True