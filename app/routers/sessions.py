from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post("/", response_model=schemas.SessionOut)
def create_session(
    session: schemas.SessionCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    obj = models.WorkoutSession(
        user_id=user.id,
        notes=session.notes,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/", response_model=list[schemas.SessionOut])
def get_sessions(db: Session = Depends(get_db)):
    return db.query(models.WorkoutSession).all()
