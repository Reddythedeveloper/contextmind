import uuid
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from typing import Dict, Any

class RAGService:
    def __init__(self, embedder: EmbeddingService, store: VectorStore):
        self.embedder = embedder
        self.store = store
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=512, chunk_overlap=64
        )

    async def ingest(self, text: str, doc_id: str, user_id: str, session_id: str, metadata: Dict[str, Any]):
        chunks = self.splitter.split_text(text)
        vectors = await self.embedder.embed(chunks)
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=v,
                payload={
                    **metadata, 
                    "text": c, 
                    "doc_id": doc_id, 
                    "user_id": user_id,
                    "session_id": session_id
                },
            )
            for c, v in zip(chunks, vectors)
        ]
        await self.store.ensure_collection(vector_size=3072)
        await self.store.upsert(points)
        return len(chunks)

    async def retrieve(self, query: str, user_id: str, session_id: str, top_k: int = 5):
        q_vec = await self.embedder.embed_query(query)
        results = await self.store.search(
            q_vec, 
            top_k=top_k,
            query_filter=Filter(must=[
                FieldCondition(key="user_id", match=MatchValue(value=user_id)),
                FieldCondition(key="session_id", match=MatchValue(value=session_id))
            ])
        )
        return [
            {
                "text": r.payload["text"], 
                "score": r.score, 
                "source": r.payload.get("filename"),
                "doc_id": r.payload.get("doc_id")
            } 
            for r in results
        ]
