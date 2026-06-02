from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import UserPersona
from app.services.llm_service import LLMService
from typing import Dict, Any, List
import json

class PersonaService:
    async def get_or_create_persona(self, db: AsyncSession, user_id: str) -> UserPersona:
        result = await db.execute(select(UserPersona).where(UserPersona.user_id == user_id))
        persona = result.scalar_one_or_none()
        if not persona:
            persona = UserPersona(user_id=user_id)
            db.add(persona)
            await db.commit()
            await db.refresh(persona)
        return persona

    async def build_system_prompt(self, persona: UserPersona) -> str:
        interests_str = ", ".join(persona.interests) if persona.interests else "none"
        recent_topics_str = ", ".join(persona.recent_topics[-5:]) if persona.recent_topics else "none"
        
        return f"""You are ContextMind, a research assistant.

User profile:
- Expertise: {persona.expertise_level}
- Preferred style: {persona.response_style}
- Interests: {interests_str}
- Recent topics: {recent_topics_str}

Adapt your responses to match this profile. Be {persona.response_style}.
When citing sources, prefer domains related to user interests if applicable.
"""

    async def update_persona_from_turn(self, db: AsyncSession, llm_service: LLMService, user_id: str, user_msg: str):
        persona = await self.get_or_create_persona(db, user_id)
        
        # Extract topics using LLM
        extraction_prompt = f"""
        Extract 1-3 main topics (short keywords) from this user message.
        User: {user_msg}
        Return JSON format: {{"topics": ["topic1", "topic2"]}}
        """
        
        # We need a non-streaming chat call here
        response = await llm_service.chat(
            messages=[{"role": "user", "content": extraction_prompt}],
            system_prompt="You are a topic extraction assistant. Only return JSON."
        )
        
        try:
            content = response.choices[0].message.content
            # Strip markdown if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            
            data = json.loads(content)
            topics = data.get("topics", [])
            
            # Update persona
            current_topics = list(persona.recent_topics or [])
            for t in topics:
                if t not in current_topics:
                    current_topics.append(t)
            
            persona.recent_topics = current_topics[-10:] # Keep last 10
            
            # Update weights
            weights = dict(persona.topic_weights or {})
            for t in topics:
                weights[t] = weights.get(t, 0) + 1
            persona.topic_weights = weights
            
            db.add(persona)
            await db.commit()
        except Exception as e:
            print(f"Error updating persona: {e}")

persona_service = PersonaService()
