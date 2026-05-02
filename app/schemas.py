from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class ExerciseCreate(BaseModel):
    name: str
    muscle_group: Optional[str] = None


class ExerciseOut(BaseModel):
    id: int
    name: str
    muscle_group: Optional[str]

    class Config:
        from_attributes = True


class SessionCreate(BaseModel):
    notes: Optional[str] = None


class SessionOut(BaseModel):
    id: int
    notes: Optional[str]
    date: datetime

    class Config:
        from_attributes = True


class SetCreate(BaseModel):
    session_id: int
    exercise_id: int
    weight: float
    reps: int
    set_number: int


class SetOut(BaseModel):
    id: int
    session_id: int
    exercise_id: int
    weight: float
    reps: int
    set_number: int

    class Config:
        from_attributes = True
