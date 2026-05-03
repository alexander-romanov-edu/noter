from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.ExerciseOut)
def create_exercise(ex: schemas.ExerciseCreate, db: Session = Depends(get_db)):
    exercise = models.Exercise(name=ex.name)
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


@router.get("/", response_model=list[schemas.ExerciseOut])
def list_exercises(db: Session = Depends(get_db)):
    return db.query(models.Exercise).all()
