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

router = APIRouter(prefix="/chat", tags=["chat"])

@router.get("/sessions")
async def list_sessions(db: AsyncSession = Depends(get_db)):
    # Mock user for now
    user_id = "user-123"
    conv_service = ConversationService(db)
    sessions = await conv_service.list_conversations(user_id)
    return sessions

@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str, db: AsyncSession = Depends(get_db)):
    conv_service = ConversationService(db)
    success = await conv_service.delete_conversation(session_id)
    if not success:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "deleted"}

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
    
    session_uuid = (await conv_service.get_or_create_conversation(user["id"], session_id)).id

    # Load initial history
    history = await conv_service.get_history(session_uuid)
    for msg in history:
        await websocket.send_json({
            "type": "history",
            "role": msg["role"],
            "content": msg["content"]
        })

    try:
        while True:
            data = await websocket.receive_text()
            print(f"DEBUG: Received WebSocket data: {data}")
            message_data = json.loads(data)
            user_message = message_data["message"]

            # 1. Build persona-aware system prompt
            persona = await persona_service.get_or_create_persona(db, user["id"])
            system_prompt = await persona_service.build_system_prompt(persona)
            print(f"DEBUG: System prompt built for user {user['id']}")

            # 2. Retrieve context from vector store (RAG)
            print(f"DEBUG: Retrieving context for query: {user_message}")
            context_chunks = await rag_service.retrieve(user_message, user["id"], session_id)
            print(f"DEBUG: Retrieved {len(context_chunks)} chunks")
            
            # Optional: Persona-weighted re-ranking could go here
            
            context_text = "\n\n".join([c["text"] for c in context_chunks])

            # 3. Build augmented message
            if context_chunks:
                context_text = "\n\n".join([f"--- SOURCE: {c['source']} ---\n{c['text']}" for c in context_chunks])
                augmented_msg = f"### DOCUMENT CONTEXT:\n{context_text}\n\n### USER QUESTION:\n{user_message}\n\n(INSTRUCTION: Use the context above to answer if relevant. Address the user directly.)"
            else:
                augmented_msg = user_message

            # 4. Load conversation history
            history = await conv_service.get_history(session_uuid)
            print(f"DEBUG: Conversation history loaded: {len(history)} messages")

            # 5. Stream LLM response
            print("DEBUG: Starting LLM stream...")
            full_response = ""
            try:
                async for token in llm_service.stream_chat(
                    messages=history + [{"role": "user", "content": augmented_msg}],
                    tools=ALL_TOOLS,
                    system_prompt=system_prompt,
                ):
                    print(f"DEBUG: Sending token: {token}")
                    await websocket.send_json({"type": "token", "content": token})
                    full_response += token
            except Exception as llm_error:
                # Fallback for tool calling errors or API issues
                print(f"LLM Error: {llm_error}")
                async for token in llm_service.stream_chat(
                    messages=history + [{"role": "user", "content": augmented_msg}],
                    system_prompt=system_prompt, # Try without tools
                ):
                    print(f"DEBUG: Sending fallback token: {token}")
                    await websocket.send_json({"type": "token", "content": token})
                    full_response += token

            print(f"DEBUG: LLM response complete. Length: {len(full_response)}")
            # 6. Save to conversation history
            await conv_service.save_message(session_uuid, "user", user_message)
            await conv_service.save_message(session_uuid, "assistant", full_response)

            # 7. Send sources
            await websocket.send_json({
                "type": "sources",
                "sources": context_chunks
            })

            # 8. Update persona (background-ish)
            await persona_service.update_persona_from_turn(db, llm_service, user["id"], user_message)
            
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()
