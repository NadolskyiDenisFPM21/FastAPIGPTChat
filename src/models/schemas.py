from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime


class AuthorRole(Enum):
    system = 'system'
    user = 'user'
    assistant = 'assistant'


class MessageBase(BaseModel):
    message: str
    model_config = ConfigDict(from_attributes=True)


class MessageCreate(MessageBase):
    message: str
    author_role: str
    thread_id: str


class MessageUserCreate(MessageCreate):
    author_role: str = 'user'


class MessageAssistantCreate(MessageCreate):
    author_role: str = 'assistant'


class MessageResponse(MessageBase):
    author_role: str
    message: Optional[str]
    model_config = ConfigDict(from_attributes=True)


class ThreadBase(BaseModel):
    id: str


class ThreadCreate(ThreadBase):
    id: str
    user_id: UUID


class TreadResponse(ThreadBase):
    id: str
    model_config = ConfigDict(from_attributes=True)

