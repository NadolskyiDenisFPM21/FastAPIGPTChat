from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, JSON, UUID
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime
from src.auth.database import User


class Thread(Base):
    __tablename__ = "thread"

    id = Column(String, primary_key=True)
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    messages = relationship("Message", back_populates="thread")
    user = relationship("User", back_populates="threads")


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    user_id = Column(UUID, ForeignKey('user.id'))
    thread_id = Column(String, ForeignKey('thread.id'))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    author_role = Column(String, nullable=False)

    user = relationship("User", back_populates="messages")
    thread = relationship("Thread", back_populates="messages")
