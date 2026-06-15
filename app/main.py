"""
Python Q&A Assistant — FastAPI Application
RAG pipeline over Stack Overflow Python Questions & Answers dataset
"""

import os
import time
import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.rag_pipeline import RAGPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global RAG pipeline instance
rag: Optional[RAGPipeline] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the RAG pipeline on startup."""
    global rag
    logger.info("Initializing RAG pipeline...")
    rag = RAGPipeline()
    rag.load_or_build_index()
    logger.info("RAG pipeline ready.")
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title="Python Q&A Assistant",
    description="AI-powered Q&A system grounded in Stack Overflow Python data",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response Models ──────────────────────────────────────────────────

class AskRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=1000,
                          example="How do I read a CSV file in Python?")
    top_k: int = Field(default=5, ge=1, le=20,
                       description="Number of retrieved context chunks")


class Source(BaseModel):
    title: str
    score: float
    snippet: str


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source]
    latency_ms: float


class HealthResponse(BaseModel):
    status: str
    index_size: int
    model: str
    version: str


# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health():
    """Check service health and index statistics."""
    if rag is None:
        raise HTTPException(status_code=503, detail="RAG pipeline not initialised")
    return HealthResponse(
        status="ok",
        index_size=rag.index_size(),
        model=rag.llm_model_name,
        version="1.0.0",
    )


@app.post("/ask", response_model=AskResponse, tags=["Q&A"])
async def ask(request: AskRequest):
    """
    Answer a Python-related question using retrieval-augmented generation.

    The system retrieves the most relevant Stack Overflow Q&A pairs and uses
    an LLM to synthesise a grounded, accurate answer.
    """
    if rag is None:
        raise HTTPException(status_code=503, detail="RAG pipeline not initialised")

    t0 = time.perf_counter()
    try:
        result = rag.answer(request.question, top_k=request.top_k)
    except Exception as exc:
        logger.exception("Error while answering question")
        raise HTTPException(status_code=500, detail=str(exc))

    latency_ms = (time.perf_counter() - t0) * 1000
    return AskResponse(
        question=request.question,
        answer=result["answer"],
        sources=result["sources"],
        latency_ms=round(latency_ms, 2),
    )


@app.get("/", tags=["System"])
async def root():
    return {"message": "Python Q&A Assistant is running. Visit /docs for the API."}
