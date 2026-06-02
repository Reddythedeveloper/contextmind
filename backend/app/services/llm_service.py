from groq import AsyncGroq
from app.core.config import settings
from typing import AsyncIterator, List, Dict, Any

# Optional LangSmith Tracing
try:
    from langsmith import traceable
except ImportError:
    def traceable(*args, **kwargs):
        return lambda f: f

class LLMService:
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"

    @traceable(name="chat_stream")
    async def stream_chat(
        self,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]] = None,
        system_prompt: str = "",
    ) -> AsyncIterator[str]:
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)

        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            tools=tools,
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]] = None,
        system_prompt: str = "",
    ) -> Any:
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)

        return await self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            tools=tools,
        )
