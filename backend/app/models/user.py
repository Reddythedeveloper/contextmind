from sqlalchemy import Column, String, DateTime, ARRAY, func
from sqlalchemy.dialects.postgresql import JSONB
from app.core.database import Base

class UserPersona(Base):
    __tablename__ = "user_personas"
    
    user_id = Column(String, primary_key=True)
    expertise_level = Column(String, default="intermediate")
    response_style = Column(String, default="detailed")
    interests = Column(ARRAY(String), default=[])
    recent_topics = Column(ARRAY(String), default=[])
    topic_weights = Column(JSONB, default={})   # topic → engagement score
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
