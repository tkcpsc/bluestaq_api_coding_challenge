import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.main import app, get_db


# Use a separate SQLite DB for API tests (file-based is simplest & reliable)
TEST_DATABASE_URL = "sqlite:///./test_api.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    """
    Ensure each test starts with a fresh schema.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    """
    Create a TestClient with a DB dependency override so API tests
    do NOT touch the real notes.db.
    """

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_create_and_get_note(client: TestClient):
    # Create
    r = client.post("/notes", json={"content": "hello api"})
    assert r.status_code == 201
    created = r.json()
    assert created["content"] == "hello api"
    assert isinstance(created["id"], int)
    assert "created_at" in created

    # Get by id
    note_id = created["id"]
    r2 = client.get(f"/notes/{note_id}")
    assert r2.status_code == 200
    fetched = r2.json()
    assert fetched["id"] == note_id
    assert fetched["content"] == "hello api"


def test_list_notes(client: TestClient):
    # Start empty
    r0 = client.get("/notes")
    assert r0.status_code == 200
    assert r0.json() == []

    # Add two notes
    client.post("/notes", json={"content": "first"})
    client.post("/notes", json={"content": "second"})

    # List should return 2
    r = client.get("/notes")
    assert r.status_code == 200
    notes = r.json()
    assert len(notes) == 2
    assert {n["content"] for n in notes} == {"first", "second"}


def test_delete_note(client: TestClient):
    # Create
    r = client.post("/notes", json={"content": "delete me"})
    note_id = r.json()["id"]

    # Delete
    d = client.delete(f"/notes/{note_id}")
    assert d.status_code == 204
    assert d.text == ""  # 204 should have no body

    # Confirm it's gone
    g = client.get(f"/notes/{note_id}")
    assert g.status_code == 404
    body = g.json()
    assert body["detail"]["error"] == "not_found"


def test_create_note_validation(client: TestClient):
    # Empty content should fail validation (FastAPI/Pydantic returns 422)
    r = client.post("/notes", json={"content": ""})
    assert r.status_code == 422


def test_delete_missing_note_returns_404(client: TestClient):
    r = client.delete("/notes/999999")
    assert r.status_code == 404
    body = r.json()
    assert body["detail"]["error"] == "not_found"