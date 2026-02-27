# Notes Vault API
### Author: Thomas Kudey
### Contact: Thomaskudeyjobs@gmail.com

## Overview

A simple RESTful API that allows users to:

* Create a note
* List all notes
* Retrieve a note by ID
* Delete a note

Built with FastAPI and SQLite. Designed for clarity, predictable behavior, and reproducibility.

---

## Tech Stack

* **FastAPI** – Web framework
* **SQLite** – Embedded relational database
* **SQLAlchemy** – ORM
* **Pytest** – Automated testing
* **Docker + Docker Compose** – Reproducible local setup

---

## API Endpoints

| Method | Endpoint    | Description       |
| ------ | ----------- | ----------------- |
| POST   | /notes      | Create a note     |
| GET    | /notes      | List all notes    |
| GET    | /notes/{id} | Get note by ID    |
| DELETE | /notes/{id} | Delete note by ID |

### Behavior

* `POST` → **201 Created**
* `GET` → **200 OK**
* `DELETE` → **204 No Content**
* Missing resource → **404 Not Found**
* Invalid input → **422 Unprocessable Entity**

---

## Data Model

**Note**

* `id` (int, primary key)
* `content` (string, 1–2000 chars)
* `created_at` (UTC timestamp)

---

## Running with Docker (Recommended)

Build and start:

```bash
docker compose up --build
```

API available at:

```
http://localhost:8000
```

Swagger docs:

```
http://localhost:8000/docs
```

Run tests:

```bash
docker compose run --rm test
```

---

## Running Without Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run tests:

```bash
python -m pytest -q
```

---

## Example Usage (curl)

Create:

```bash
curl -X POST http://localhost:8000/notes \
  -H "Content-Type: application/json" \
  -d '{"content":"Example note"}'
```

List:

```bash
curl http://localhost:8000/notes
```

---

## Assumptions & Tradeoffs

* No authentication required
* SQLite chosen for simplicity
* Tables created at startup (no migrations)
* No update/search endpoints (not required)

---

## Project Structure

```
app/
  main.py
  crud.py
  models.py
  schemas.py
  db.py

tests/
Dockerfile
docker-compose.yml
```

---
