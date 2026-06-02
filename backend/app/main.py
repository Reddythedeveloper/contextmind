from fastapi import FastAPI
from app.core.config import settings
from app.api import documents, chat

app = FastAPI(title="ContextMind API")

app.include_router(documents.router)
app.include_router(chat.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
