from datetime import datetime, timedelta, timezone

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Text)
from sqlalchemy.orm import relationship

from database import Base

msc_timezone = timezone(timedelta(hours=3))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    notes = relationship("Note", back_populates="owner", cascade="all, delete")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)

    pinned = Column(Boolean, default=False)
    tags = Column(String, default="")

    created_at = Column(DateTime, default=datetime.now(msc_timezone))
    updated_at = Column(DateTime, default=datetime.now(msc_timezone))

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="notes")
