import uuid

from fastapi import FastAPI, Depends
from fastapi_users import fastapi_users, FastAPIUsers

from .auth.auth import auth_backend
from .auth.database import User
from .auth.manager import get_user_manager
from .auth.schemas import UserRead, UserCreate
from .gpt_client.router import openai_router


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)


app = FastAPI()

app.include_router(openai_router)
current_user = fastapi_users.current_user()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


