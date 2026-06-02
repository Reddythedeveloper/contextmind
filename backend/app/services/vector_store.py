from qdrant_client import AsyncQdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter
from app.core.config import settings
from typing import List, Dict, Any, Optional

class VectorStore:
    def __init__(self):
        self.client = AsyncQdrantClient(url=settings.QDRANT_URL)
        self.collection = "documents"

    async def ensure_collection(self, vector_size: int = 3072):
        # gemini-embedding-2 size is 3072
        collections = await self.client.get_collections()
        names = [c.name for c in collections.collections]
        if self.collection not in names:
            await self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )

    async def upsert(self, points: List[PointStruct]):
        await self.client.upsert(collection_name=self.collection, points=points)

    async def search(self, query_vector: List[float], top_k: int = 5, query_filter: Optional[Filter] = None):
        return await self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=top_k,
            query_filter=query_filter,
        )
