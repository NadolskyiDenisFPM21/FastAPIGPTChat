import uuid

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_async_session
from .models import Message, Thread
from .schemas import MessageCreate, MessageResponse, TreadResponse, ThreadCreate


async def add_message_db(message: MessageCreate, user_id: uuid.UUID):
    async for session in get_async_session():
        message = Message(**message.model_dump())
        message.user_id = user_id
        session.add(message)
        await session.commit()
        await session.refresh(message)
        return MessageResponse.model_validate(message)


async def get_all_user_messages(user_id: uuid.UUID):
    async for session in get_async_session():
        query = select(Message).where(Message.user_id == user_id)
        messages = await session.execute(query)
        messages = messages.scalars().all()
        return [MessageResponse.model_validate(message) for message in messages]


async def add_thread_db(thread: ThreadCreate):
    async for session in get_async_session():
        thread = Thread(**thread.model_dump())
        session.add(thread)
        await session.commit()
        await session.refresh(thread)
        return TreadResponse.model_validate(thread)

