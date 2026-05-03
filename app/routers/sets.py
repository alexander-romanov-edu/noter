from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/sets", tags=["Sets"])


@router.post("/", response_model=schemas.SetOut)
def create_set(data: schemas.SetCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    obj = models.WorkoutSet(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/", response_model=list[schemas.SetOut])
def get_sets(db: Session = Depends(get_db)):
    return db.query(models.Set).all()

@router.put("/{set_id}", response_model=schemas.SetOut)
def update_set(set_id: int, data: schemas.SetUpdate, db: Session = Depends(get_db)):
    obj = db.query(models.WorkoutSet).get(set_id)

    if not obj:
        raise HTTPException(404)

    for k, v in data.dict(exclude_unset=True).items():
        setattr(obj, k, v)

    db.commit()
    return obj


@router.delete("/{set_id}")
def delete_set(set_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.WorkoutSet).get(set_id)

    if not obj:
        raise HTTPException(404)

    db.delete(obj)
    db.commit()
    return {"ok": True}
