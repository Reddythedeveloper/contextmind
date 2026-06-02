from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from app.models.conversation import Conversation, Message
from typing import List, Dict, Any
import uuid

class ConversationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_conversation(self, user_id: str, session_id: str) -> Conversation:
        result = await self.db.execute(
            select(Conversation).where(Conversation.session_id == session_id)
        )
        conv = result.scalar_one_or_none()
        if conv:
            return conv
        
        conv = Conversation(session_id=session_id, user_id=user_id)
        self.db.add(conv)
        await self.db.commit()
        await self.db.refresh(conv)
        return conv

    async def get_conversation_with_docs(self, session_id: str) -> Conversation:
        from sqlalchemy.orm import selectinload
        result = await self.db.execute(
            select(Conversation)
            .options(selectinload(Conversation.documents), selectinload(Conversation.messages))
            .where(Conversation.session_id == session_id)
        )
        return result.scalar_one_or_none()

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

    async def list_conversations(self, user_id: str) -> List[Conversation]:
        result = await self.db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(desc(Conversation.created_at))
        )
        return result.scalars().all()

    async def delete_conversation(self, session_id: str):
        result = await self.db.execute(
            select(Conversation).where(Conversation.session_id == session_id)
        )
        conv = result.scalar_one_or_none()
        if conv:
            await self.db.delete(conv)
            await self.db.commit()
            return True
        return False
