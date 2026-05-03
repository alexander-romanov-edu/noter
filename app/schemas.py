from pydantic import BaseModel, EmailStr

from datetime import datetime



class SetUpdate(BaseModel):
    weight: int | None = None
    reps: int | None = None
class SetCreate(BaseModel):
    session_id: int
    exercise_id: int
    weight: int
    reps: int


class SetOut(BaseModel):
    id: int
    session_id: int
    exercise_id: int
    weight: int
    reps: int

    class Config:
        from_attributes = True
class SessionCreate(BaseModel):
    pass  # no input needed, just create session


class SessionOut(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class ExerciseCreate(BaseModel):
    name: str

class ExerciseOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
