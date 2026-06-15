<<<<<<< HEAD
# Python Programming Q&A Assistant

## Overview
AI-powered question answering system for Python learners using RAG.

## Tech Stack
- FastAPI
- LangChain
- ChromaDB/FAISS
- OpenAI/Gemini
- Python

## Architecture
[diagram]

## API Endpoints

### POST /ask

Request:
{
  "question": "What is list comprehension?"
}

Response:
{
  "answer": "..."
}

### GET /health

Response:
{
  "status": "healthy"
}

## Deployment

Live URL:
https://your-app-url.com

## Setup

pip install -r requirements.txt

uvicorn app.main:app --reload
=======
# Python Q&A Assistant 🐍

An AI-powered question-answering system grounded in Stack Overflow Python data, built with a RAG pipeline and served via FastAPI.

---

## Architecture

```
User Question
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│                      FastAPI Service                    │
│                                                         │
│  POST /ask                         GET /health          │
│      │                                                  │
│      ▼                                                  │
│  ┌───────────────────────────────────────────────────┐  │
│  │                   RAG Pipeline                    │  │
│  │                                                   │  │
│  │  1. Embed query  (sentence-transformers local)    │  │
│  │       │                                           │  │
│  │       ▼                                           │  │
│  │  2. Retrieve top-k chunks  (FAISS IndexFlatIP)    │  │
│  │       │                                           │  │
│  │       ▼                                           │  │
│  │  3. Build prompt with context                     │  │
│  │       │                                           │  │
│  │       ▼                                           │  │
│  │  4. Generate answer  (OpenAI-compatible LLM)      │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
     │
     ▼
JSON Response  { question, answer, sources, latency_ms }
```

**Embedding model:** `all-MiniLM-L6-v2` (runs locally, no API key needed)  
**Vector store:** FAISS `IndexFlatIP` (cosine similarity via normalised inner product)  
**LLM:** `llama-3.3-70b-versatile (Groq)` via OpenAI API (swappable via env vars for Groq, Together, Ollama…)  
**Dataset:** Stack Overflow Python Questions & Answers (Kaggle)

---

## Quick Start

### 1 — Clone & configure

```bash
git clone https://github.com/<your-username>/python-qa-assistant.git
cd python-qa-assistant
cp .env.example .env
# Edit .env — at minimum set GROQ_API_KEY
```

### 2 — Download the dataset

```bash
# Option A: Kaggle CLI  (recommended)
pip install kaggle
python scripts/download_data.py

# Option B: Manual
# Download from https://www.kaggle.com/datasets/stackoverflow/pythonquestions
# Extract Questions.csv and Answers.csv into ./data/
```

> **No dataset?** The server starts with a built-in 30-row sample so you can test immediately.
> Download the full dataset for production-quality answers.

### 3 — Install & run

```bash
# Option A: Local Python
pip install -r requirements.txt
uvicorn app.main:app --reload

# Option B: Docker Compose
docker compose up --build
```

The API is now live at `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs`

---

## API Reference

### `GET /health`

```json
{
  "status": "ok",
  "index_size": 48723,
  "model": "llama-3.3-70b-versatile (Groq)",
  "version": "1.0.0"
}
```

### `POST /ask`

**Request**
```json
{
  "question": "How do I read a CSV file in Python?",
  "top_k": 5
}
```

**Response**
```json
{
  "question": "How do I read a CSV file in Python?",
  "answer": "You can read a CSV file using pandas...",
  "sources": [
    {
      "title": "Read CSV into pandas DataFrame",
      "score": 0.912,
      "snippet": "import pandas as pd\ndf = pd.read_csv('file.csv')..."
    }
  ],
  "latency_ms": 843.12
}
```

| Field | Type | Description |
|---|---|---|
| `question` | string | 5–1000 characters |
| `top_k` | int | 1–20, default 5 — retrieved context chunks |

---

## Running Tests

```bash
pytest tests/ -v
```

28 tests covering health checks, core Q&A flow, 10 diverse Python queries, edge cases, and input validation.

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `GROQ_API_KEY` | — | **Required.** LLM API key |
| `LLM_MODEL` | `llama-3.3-70b-versatile (Groq)` | Model name |
| `OPENAI_BASE_URL` | OpenAI default | Override for Groq / Together / Ollama |
| `EMBED_MODEL` | `all-MiniLM-L6-v2` | Sentence-transformers model |
| `DATA_DIR` | `data` | Folder with `Questions.csv` / `Answers.csv` |
| `INDEX_DIR` | `index` | FAISS index persistence folder |
| `MAX_DOCS` | `50000` | Max rows to index |
| `MAX_CONTEXT_DOCS` | `5` | Context chunks sent to LLM |

---

## Deployment

### Render / Railway
1. Push to GitHub
2. Connect repo → set env vars in dashboard
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Hugging Face Spaces
Use the `Dockerfile` — HF Spaces supports Docker deployments natively.

### Cost note
With `llama-3.3-70b-versatile (Groq)`, a typical `/ask` call uses ~800 input + ~300 output tokens ≈ **$0.0002** per request.

---

## Scaling to 100+ Concurrent Users

See the slide deck (`slides/`) for the full architecture diagram. Key points:

| Concern | Solution |
|---|---|
| **Async I/O** | Run LLM calls with `asyncio` / `httpx.AsyncClient` |
| **LLM latency** | Use streaming responses; cache common queries in Redis |
| **Vector search** | FAISS is in-memory and thread-safe for reads; no bottleneck below 10M docs |
| **Workers** | `uvicorn --workers 4` or Gunicorn + uvicorn workers |
| **Horizontal scale** | Deploy behind a load balancer; share index via a mounted volume or a managed vector DB (Pinecone, Weaviate) |
| **Cost** | Batch similar queries; cache semantic-nearest duplicates |

---

## Project Structure

```
python-qa-assistant/
├── app/
│   ├── main.py          # FastAPI app, endpoints, models
│   └── rag_pipeline.py  # Embedding, FAISS index, LLM generation
├── tests/
│   └── test_api.py      # 28 pytest tests
├── scripts/
│   └── download_data.py # Kaggle dataset downloader
├── data/                # CSVs go here (git-ignored)
├── index/               # FAISS index (git-ignored)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── .env.example
└── README.md
```
>>>>>>> 30d3c83 (upload project folder)
