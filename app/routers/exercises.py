from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter(prefix="/exercises", tags=["Exercises"])


@router.post("/")
def create_exercise(name: str, muscle_group: str, db: Session = Depends(get_db)):
    exercise = models.Exercise(name=name, muscle_group=muscle_group)
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise


@router.get("/")
def get_exercises(db: Session = Depends(get_db)):
    return db.query(models.Exercise).all()
