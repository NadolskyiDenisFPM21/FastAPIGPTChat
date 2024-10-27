import asyncio
import uuid
from typing import List, Dict

from openai import AsyncOpenAI
from openai.types.beta import Assistant

from src.config import settings


class OpenAIManager:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.system_message = {'role': 'system', 'content': 'Відповідай виключно українською мовою.'}
        self.assistant = None

    async def create_assistant(self):
        self.assistant = await self.client.beta.assistants.create(
            name='Polyservice Bot',
            instructions='Відповідай виключно українською мовою.',
            model=settings.GPT_MODEL,
        )

    async def create_thread(self):
        return (await self.client.beta.threads.create()).id

    async def send_message(self, message: str, thread_id: str):
        if not self.assistant:
            await self.create_assistant()

        message = await self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message
        )
        run = await self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=self.assistant.id
        )
        messages = await self.client.beta.threads.messages.list(thread_id=thread_id)
        ai_response: str = ''
        async for message in messages:
            if message.role == 'assistant':
                ai_response = message.content[0].text.value
                break

        return ai_response


ai_client = OpenAIManager(api_key=settings.OPENAI_API_KEY)

