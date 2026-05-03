from sqlalchemy import Column, Integer, Text, DateTime, Boolean, String
from datetime import datetime
from database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)

    pinned = Column(Boolean, default=False)
    tags = Column(String, default="")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
