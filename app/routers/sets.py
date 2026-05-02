from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/sets", tags=["Sets"])


@router.post("/", response_model=schemas.SetOut)
def create_set(
    set_data: schemas.SetCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    obj = models.WorkoutSet(**set_data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/", response_model=list[schemas.SetOut])
def get_sets(db: Session = Depends(get_db)):
    return db.query(models.WorkoutSet).all()
