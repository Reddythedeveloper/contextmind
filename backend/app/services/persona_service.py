from typing import Dict, Any

class PersonaService:
    async def build_system_prompt(self, user: Dict[str, Any]) -> str:
        # Placeholder for real persona logic in Phase 4
        return f"""You are ContextMind, a research assistant.
Expertise: intermediate
Style: detailed
"""

persona_service = PersonaService()
