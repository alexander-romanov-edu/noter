from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/one-rep-max/{exercise_id}")
def one_rep_max(exercise_id: int, db: Session = Depends(get_db)):
    sets = db.query(models.WorkoutSet).filter_by(exercise_id=exercise_id).all()

    best = 0
    for s in sets:
        est = s.weight * (1 + s.reps / 30)
        best = max(best, est)

    return {"exercise_id": exercise_id, "1rm": best}


@router.get("/volume/{exercise_id}")
def volume(exercise_id: int, db: Session = Depends(get_db)):
    sets = db.query(models.WorkoutSet).filter_by(exercise_id=exercise_id).all()

    total = sum(s.weight * s.reps for s in sets)

    return {"exercise_id": exercise_id, "volume": total}
