from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from database import SessionLocal, engine
from models import Base, Note

app = FastAPI()

Base.metadata.create_all(bind=engine)


# --- Pydantic schemas ---
class NoteCreate(BaseModel):
    content: str


class NoteResponse(BaseModel):
    id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True  # replaces orm_mode in newer Pydantic


# --- DB dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Routes ---

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")

# GET all notes
@app.get("/notes", response_model=List[NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    return db.query(Note).order_by(Note.created_at).all()


# POST create note
@app.post("/notes", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    if not note.content.strip():
        raise HTTPException(status_code=400, detail="Empty note")

    db_note = Note(content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


# DELETE note
@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()
    db.refresh(db_note)
    return {"message": "deleted"}

from fastapi import Body

# UPDATE note
@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    updated: NoteCreate = Body(...),
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if not updated.content.strip():
        raise HTTPException(status_code=400, detail="Empty note")

    note.content = updated.content
    db.commit()
    db.refresh(note)

    return note
