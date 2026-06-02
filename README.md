# 🧠 ContextMind — Personalized Conversational AI Research Assistant

ContextMind is a full-stack GenAI application that combines conversational AI, semantic vector search, real-time document ingestion, and user personalization.

## 🚀 Tech Stack

- **LLM:** Groq (Llama 3.3 70B) for Conversational AI & Tool Calling
- **Embeddings:** Google Gemini (gemini-embedding-2)
- **Vector DB:** Qdrant
- **Backend:** FastAPI (Python 3.11)
- **Frontend:** Next.js 14 + Tailwind CSS + Lucide React
- **Database:** PostgreSQL (SQLAlchemy)
- **Cache:** Redis
- **CI/CD:** GitHub Actions

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                         CONTEXTMIND                                │
│                                                                    │
│  ┌──────────────┐    REST/WS     ┌──────────────────────────────┐  │
│  │  Next.js 14  │ ◄────────────► │        FastAPI Backend       │  │
│  │  (Frontend)  │                │                              │  │
│  └──────────────┘                │  ┌──────────────────────┐    │  │
│                                  │  │  Conversation Engine  │    │  │
│  ┌──────────────┐                │  │  - History Manager   │    │  │
│  │  PostgreSQL  │ ◄──────────── │  │  - Persona Tracker   │    │  │
│  │  (Sessions   │                │  │  - Tool Dispatcher   │    │  │
│  │   + Prefs)   │                │  └──────────────────────┘    │  │
│  └──────────────┘                │                              │  │
│                                  │  ┌──────────────────────┐    │  │
│  ┌──────────────┐                │  │    RAG Pipeline       │    │  │
│  │    Redis     │ ◄──────────── │  │  - Chunker           │    │  │
│  │  (Sessions   │                │  │  - Embedder          │    │  │
│  │   + Cache)   │                │  │  - Retriever         │    │  │
│  └──────────────┘                │  └──────────────────────┘    │  │
│                                  │                              │  │
│  ┌──────────────┐                │  ┌──────────────────────┐    │  │
│  │    Qdrant    │ ◄──────────── │  │   Personalization    │    │  │
│  │  (Vector DB) │                │  │   Engine             │    │  │
│  └──────────────┘                │  └──────────────────────┘    │  │
│                                  │             │                 │  │
│  ┌──────────────────────────┐    │             ▼                 │  │
│  │   LLM Layer              │ ◄──│       Groq / Gemini          │  │
│  │   (Llama 3 / Gemini)     │    │   + Function Calling         │  │
│  └──────────────────────────┘    └──────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

## 🛠️ Local Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/Reddythedeveloper/contextmind.git
   cd contextmind
   ```

2. **Environment Variables**
   Copy `.env.example` to `backend/.env` and fill in your keys:
   - `GROQ_API_KEY`
   - `GEMINI_API_KEY`

3. **Start Services**
   ```bash
   docker compose up -d
   ```

4. **Run Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # venv\Scripts\activate on Windows
   pip install -r requirements.txt
   alembic upgrade head
   python -m app.main
   ```

5. **Run Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 🌟 Core Features

- **Personalization Engine:** Extracts topics from your conversations to build a unique persona.
- **RAG Integration:** Upload PDF, DOCX, or TXT files to ground the AI in your specific documents.
- **Real-time Streaming:** Smooth, token-by-token WebSocket streaming.
- **Source Citations:** Every AI claim includes a citation to the specific document chunk.

## 🧪 Testing

```bash
cd backend
pytest tests/ -v
```
