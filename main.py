from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from database import SessionLocal, engine
from models import Base, Note

app = FastAPI()

Base.metadata.create_all(bind=engine)


class NoteCreate(BaseModel):
    content: str


class NoteResponse(BaseModel):
    id: int
    content: str
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

@app.get("/notes", response_model=List[NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    return db.query(Note).order_by(Note.created_at).all()


@app.post("/notes", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    if not note.content.strip():
        raise HTTPException(status_code=400, detail="Empty note")

    db_note = Note(
        content=note.content,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()
    db.refresh(db_note)
    return {"message": "deleted"}


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
    note.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(note)

    return note
