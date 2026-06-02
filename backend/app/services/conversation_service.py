from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from app.models.conversation import Conversation, Message
from typing import List, Dict, Any
import uuid

class ConversationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_conversation(self, user_id: str, conversation_id: uuid.UUID = None) -> Conversation:
        if conversation_id:
            result = await self.db.execute(select(Conversation).where(Conversation.id == conversation_id))
            conv = result.scalar_one_or_none()
            if conv:
                return conv
        
        conv = Conversation(id=conversation_id or uuid.uuid4(), user_id=user_id)
        self.db.add(conv)
        await self.db.commit()
        await self.db.refresh(conv)
        return conv

    async def get_history(self, conversation_id: uuid.UUID, limit: int = 10) -> List[Dict[str, Any]]:
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(desc(Message.created_at))
            .limit(limit)
        )
        messages = result.scalars().all()
        # Reverse to get chronological order
        return [{"role": m.role, "content": m.content} for m in reversed(messages)]

    async def save_message(self, conversation_id: uuid.UUID, role: str, content: str, tool_calls: Any = None):
        msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_calls=tool_calls
        )
        self.db.add(msg)
        await self.db.commit()
        return msg
