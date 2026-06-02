import pytest
from app.services.rag_service import RAGService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.core.config import settings

@pytest.mark.asyncio
async def test_ingest_and_retrieve():
    # This test requires real API keys and Qdrant running
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_gemini_key":
        pytest.skip("GEMINI_API_KEY not set")
    
    embedder = EmbeddingService()
    store = VectorStore()
    rag_service = RAGService(embedder, store)
    
    doc_text = "FastAPI is a modern Python web framework for building APIs."
    user_id = "test-user"
    doc_id = "test-doc"
    
    # Clean up or use a unique user_id
    num_chunks = await rag_service.ingest(doc_text, doc_id, user_id, {"filename": "test.txt"})
    assert num_chunks > 0
    
    results = await rag_service.retrieve("What is FastAPI?", user_id)
    assert len(results) > 0
    assert "FastAPI" in results[0]["text"]
    assert results[0]["score"] > 0.5
