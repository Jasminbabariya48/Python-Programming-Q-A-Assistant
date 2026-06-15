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
