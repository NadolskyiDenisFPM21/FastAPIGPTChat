from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from src.models.database import Base, get_async_session


class User(SQLAlchemyBaseUserTableUUID, Base):
    messages = relationship("Message", back_populates="user")
    threads = relationship("Thread", back_populates="user")


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

