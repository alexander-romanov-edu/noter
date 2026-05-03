from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, Note, User

app = FastAPI()

Base.metadata.create_all(bind=engine)

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCreate(BaseModel):
    username: str
    password: str


class NoteCreate(BaseModel):
    content: str
    tags: str = ""


class NoteUpdate(BaseModel):
    content: str
    pinned: bool
    tags: str


class NoteResponse(BaseModel):
    id: int
    content: str
    pinned: bool
    tags: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(401, "Missing token")

    try:
        scheme, token = authorization.split()
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        raise HTTPException(401, "Invalid token")

    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(401, "User not found")

    return user


@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")


@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter_by(username=user.username).first():
        raise HTTPException(400, "User exists")

    new_user = User(username=user.username, password_hash=hash_password(user.password))

    db.add(new_user)
    db.commit()
    return {"message": "ok"}


@app.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(username=user.username).first()

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/notes")
def get_notes(
    limit: int = 5,
    offset: int = 0,
    search: str | None = None,
    sort: str = "newest",
    tag: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    query = db.query(Note).filter(Note.owner_id == user.id)

    if search:
        query = query.filter(Note.content.ilike(f"%{search}%"))

    if tag:
        query = query.filter(Note.tags.ilike(f"%{tag}%"))

    if sort == "newest":
        query = query.order_by(Note.pinned.desc(), Note.created_at.desc())
    elif sort == "oldest":
        query = query.order_by(Note.pinned.desc(), Note.created_at.asc())
    elif sort == "az":
        query = query.order_by(Note.pinned.desc(), Note.content.asc())
    elif sort == "za":
        query = query.order_by(Note.pinned.desc(), Note.content.desc())

    return query.offset(offset).limit(limit).all()


@app.post("/notes", response_model=NoteResponse)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_note = Note(
        content=note.content,
        tags=note.tags,
        pinned=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        owner_id=user.id,
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    updated: NoteUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    note = db.query(Note).filter_by(id=note_id, owner_id=user.id).first()
    if not note:
        raise HTTPException(404)

    note.content = updated.content
    note.tags = updated.tags
    note.pinned = updated.pinned
    note.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(note)
    return note


@app.delete("/notes/{note_id}")
def delete_note(
    note_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    note = db.query(Note).filter_by(id=note_id, owner_id=user.id).first()
    if not note:
        raise HTTPException(404)

    db.delete(note)
    db.commit()
    return {"ok": True}
