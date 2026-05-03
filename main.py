from fastapi import FastAPI, Depends, HTTPException, Body, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from database import SessionLocal, engine
from models import Base, Note

app = FastAPI()

Base.metadata.create_all(bind=engine)


class NoteCreate(BaseModel):
    content: str


class NoteUpdate(BaseModel):
    content: str
    pinned: bool = False


class NoteResponse(BaseModel):
    id: int
    content: str
    pinned: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")


@app.get("/notes")
def get_notes(
    db: Session = Depends(get_db),
    limit: int = 10,
    offset: int = 0,
    search: str | None = None,
    sort: str = "newest"
):
    query = db.query(Note)

    if search:
        query = query.filter(Note.content.ilike(f"%{search}%"))
    if sort == "newest":
        query = query.order_by(Note.pinned.desc(), Note.created_at.desc())
    elif sort == "oldest":
        query = query.order_by(Note.pinned.desc(), Note.created_at.asc())
    elif sort == "az":
        query = query.order_by(Note.pinned.desc(), Note.content.asc())
    elif sort == "za":
        query = query.order_by(Note.pinned.desc(), Note.content.desc())
    notes = query.offset(offset).limit(limit).all()
    return notes
@app.post("/notes", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    if not note.content.strip():
        raise HTTPException(status_code=400, detail="Empty note")

    db_note = Note(
        content=note.content,
        pinned=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    updated: NoteUpdate,
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if not updated.content.strip():
        raise HTTPException(status_code=400, detail="Empty note")

    note.content = updated.content
    note.pinned = updated.pinned
    note.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(note)

    return note


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()

    return {"message": "deleted"}
