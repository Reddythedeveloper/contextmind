from fastapi import APIRouter, WebSocket, Depends, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.llm_service import LLMService
from app.services.rag_service import RAGService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.conversation_service import ConversationService
from app.services.persona_service import persona_service
from app.services.tool_service import ALL_TOOLS
import json
import uuid

router = APIRouter(prefix="/chat", tags=["chat"])

@router.websocket("/ws/{session_id}")
async def chat_ws(
    websocket: WebSocket,
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    await websocket.accept()
    
    # Mock user for now
    user = {"id": "user-123", "email": "test@example.com"}
    
    llm_service = LLMService()
    embedder = EmbeddingService()
    store = VectorStore()
    rag_service = RAGService(embedder, store)
    conv_service = ConversationService(db)
    
    session_uuid = uuid.UUID(session_id)
    await conv_service.get_or_create_conversation(user["id"], session_uuid)

    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            user_message = message_data["message"]

            # 1. Build persona-aware system prompt
            system_prompt = await persona_service.build_system_prompt(user)

            # 2. Retrieve context from vector store (RAG)
            context_chunks = await rag_service.retrieve(user_message, user["id"])
            context_text = "\n\n".join([c["text"] for c in context_chunks])

            # 3. Build augmented message
            augmented_msg = f"Context from your documents:\n{context_text}\n\nQuestion: {user_message}"

            # 4. Load conversation history
            history = await conv_service.get_history(session_uuid)

            # 5. Stream LLM response
            full_response = ""
            async for token in llm_service.stream_chat(
                messages=history + [{"role": "user", "content": augmented_msg}],
                tools=ALL_TOOLS,
                system_prompt=system_prompt,
            ):
                await websocket.send_json({"type": "token", "content": token})
                full_response += token

            # 6. Save to conversation history
            await conv_service.save_message(session_uuid, "user", user_message)
            await conv_service.save_message(session_uuid, "assistant", full_response)

            # 7. Send sources
            await websocket.send_json({
                "type": "sources",
                "sources": context_chunks
            })
            
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()
