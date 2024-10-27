import uuid

from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers

from .manager import ai_client
from ..auth.auth import auth_backend
from ..auth.database import User
from ..auth.manager import get_user_manager
from ..models.crud import get_all_user_messages, add_message_db, add_thread_db, get_all_user_threads_db, \
    get_all_thread_messages_db, delete_thread_db
from ..models.models import Thread
from ..models.schemas import MessageResponse, MessageCreate, ThreadCreate, MessageUserCreate, MessageAssistantCreate

openai_router = APIRouter(prefix='/chat')

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


@openai_router.post('/thread')
async def create_thread(user: User = Depends(current_user)):
    tread_id = await ai_client.create_thread()
    print(tread_id)
    thread = ThreadCreate(
        id=tread_id,
        user_id=user.id,
    )
    return await add_thread_db(thread)


@openai_router.get('/thread')
async def get_all_user_threads(user: User = Depends(current_user)):
    threads = await get_all_user_threads_db(user.id)
    return threads


@openai_router.get('/thread/{thread_id}')
async def get_all_thread_message(thread_id: str, user: User = Depends(current_user)):
    messages = await get_all_thread_messages_db(thread_id)
    return messages


@openai_router.delete('/thread/{thread_id}')
async def delete_thread(thread_id: str, user: User = Depends(current_user)):
    return await delete_thread_db(thread_id)


@openai_router.post('/thread/{thread_id}')
async def send_message(message: MessageUserCreate = Depends(),
                       user: User = Depends(current_user)):
    response = await ai_client.send_message(message.message, message.thread_id)
    response_message = MessageAssistantCreate(
        message=response,
        thread_id=message.thread_id,
    )
    await add_message_db(message, user.id)
    await add_message_db(response_message, user.id)

    return response

