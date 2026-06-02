from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.persona_service import persona_service
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/users", tags=["users"])

class PersonaUpdate(BaseModel):
    expertise_level: Optional[str] = None
    response_style: Optional[str] = None
    interests: Optional[List[str]] = None

@router.get("/persona")
async def get_persona(db: AsyncSession = Depends(get_db)):
    # Mock user for now
    user_id = "user-123"
    persona = await persona_service.get_or_create_persona(db, user_id)
    return persona

@router.post("/persona")
async def update_persona(update: PersonaUpdate, db: AsyncSession = Depends(get_db)):
    # Mock user for now
    user_id = "user-123"
    persona = await persona_service.get_or_create_persona(db, user_id)
    
    if update.expertise_level:
        persona.expertise_level = update.expertise_level
    if update.response_style:
        persona.response_style = update.response_style
    if update.interests is not None:
        persona.interests = update.interests
        
    db.add(persona)
    await db.commit()
    await db.refresh(persona)
    return persona
