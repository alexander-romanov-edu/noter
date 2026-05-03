# 📝 Noter app

A simple notes application built with **FastAPI**, **SQLAlchemy**, **JWT authentication**, and a minimal web UI.
Supports creating, editing, deleting, pinning, tagging, searching, and paginated notes.

---

# 🚀 Features

* User authentication (JWT)
* Create / edit / delete notes
* Pin important notes
* Tags + filtering
* Search notes
* Pagination
* Simple HTML + JS frontend
* SQLite (default) or other SQLAlchemy DB

---

# 📦 Project Structure

```
.
├── main.py
├── models.py
├── database.py
├── static/
│   └── index.html
├── tests/
│   └── test_notes.py
├── flake.nix
└── README.md
```

---

# ⚙️ Setup

## 🟢 Option 1: With Nix (recommended)

### 1. Enter dev environment

```bash
nix develop
```

---

### 2. Run the server

```bash
uvicorn main:app --reload
```

Open:

```
http://127.0.0.1:8000
```

---

### 3. Run tests

```bash
python -m pytest
```

---

### (Optional) auto shell activation

If using `direnv`:

```bash
direnv allow
```

---

## 🟡 Option 2: Without Nix (pip/venv)

### 1. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run server

```bash
uvicorn main:app --reload
```

---

### 4. Run tests

```bash
pytest
```

---

# 🧪 Running Tests

Tests use `pytest` and FastAPI `TestClient`.

Run:

```bash
pytest -v
```

To debug imports:

```bash
PYTHONPATH=. pytest
```

---

# 🖥️ Running the App

Start server:

```bash
uvicorn main:app --reload
```

Then open:

```
http://127.0.0.1:8000
```

---

# 🔐 Authentication

The app uses JWT tokens.

Flow:

1. Register user
2. Login
3. Receive token
4. Use token in requests:

```http
Authorization: Bearer <token>
```

---

# 🧱 Tech Stack

* FastAPI
* SQLAlchemy
* SQLite (default)
* JWT (python-jose)
* bcrypt (password hashing)
* pytest (testing)
* Vanilla HTML/JS frontend

---

# 🧪 Example API

### Create note

```http
POST /notes
Authorization: Bearer <token>

{
  "content": "My note"
}
```

---

### Get notes

```http
GET /notes?limit=10&offset=0
```

---

### Delete note

```http
DELETE /notes/{id}
```

---

# 🧰 Development Notes

## Linting

(Optional)

```bash
pylint . --ignore=.venv
```

---

# 🧊 Nix Flake

This project includes a reproducible dev environment:

```bash
nix develop
```

Everything (Python + dependencies) is preinstalled.

---

# 📌 Future improvements

* Alembic migrations
* React frontend
* Docker support
* CI pipeline (GitHub Actions)
* Role-based access control

---

# 📄 License

MIT
