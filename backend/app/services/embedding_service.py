import google.generativeai as genai
from app.core.config import settings
from typing import List

class EmbeddingService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = "models/gemini-embedding-2"

    async def embed(self, texts: List[str]) -> List[List[float]]:
        # Gemini embed_content is not async, but we can wrap it if needed.
        # For simplicity in this blueprint implementation, we'll call it directly.
        # In a real high-load app, we might use a thread pool.
        results = []
        for text in texts:
            embedding = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_document"
            )
            results.append(embedding["embedding"])
        return results

    async def embed_query(self, text: str) -> List[float]:
        embedding = genai.embed_content(
            model=self.model,
            content=text,
            task_type="retrieval_query"
        )
        return embedding["embedding"]
