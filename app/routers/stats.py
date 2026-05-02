from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/one-rep-max/{exercise_id}")
def one_rep_max(exercise_id: int, db: Session = Depends(get_db)):
    sets = db.query(models.WorkoutSet).filter(
        models.WorkoutSet.exercise_id == exercise_id
    ).all()

    best_1rm = 0

    for s in sets:
        estimated = s.weight * (1 + s.reps / 30)
        best_1rm = max(best_1rm, estimated)

    return {"exercise_id": exercise_id, "estimated_1rm": best_1rm}
