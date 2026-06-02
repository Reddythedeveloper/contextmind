from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.services.rag_service import RAGService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
import PyPDF2
import docx
import io
import uuid

router = APIRouter(prefix="/documents", tags=["documents"])

# Dependency injection
def get_rag_service():
    embedder = EmbeddingService()
    store = VectorStore()
    return RAGService(embedder, store)

# Mock user dependency
async def get_current_user():
    return {"id": "user-123", "email": "test@example.com"}

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service)
):
    content = await file.read()
    filename = file.filename
    text = ""

    if filename.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        for page in pdf_reader.pages:
            text += page.extract_text()
    elif filename.endswith(".docx"):
        doc = docx.Document(io.BytesIO(content))
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif filename.endswith(".txt"):
        text = content.decode("utf-8")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    doc_id = str(uuid.uuid4())
    num_chunks = await rag_service.ingest(
        text=text,
        doc_id=doc_id,
        user_id=user["id"],
        metadata={"filename": filename}
    )

    return {
        "message": "Document uploaded and indexed",
        "doc_id": doc_id,
        "chunks": num_chunks
    }

@router.get("/search")
async def search_documents(
    q: str,
    user: dict = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service)
):
    results = await rag_service.retrieve(query=q, user_id=user["id"])
    return {"results": results}
