from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post("/", response_model=schemas.SessionOut)
def create_session(data: schemas.SessionCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    obj = models.WorkoutSession(user_id=user.id, notes=data.notes)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/", response_model=list[schemas.SessionOut])
def get_sessions(db: Session = Depends(get_db)):
    return db.query(models.WorkoutSession).all()


@router.delete("/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    obj = db.query(models.WorkoutSession).get(session_id)

    if not obj:
        raise HTTPException(404)

    if obj.user_id != user.id:
        raise HTTPException(403)

    db.delete(obj)
    db.commit()
    return {"ok": True}
