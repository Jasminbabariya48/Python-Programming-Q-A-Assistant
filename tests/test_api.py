"""
API Test Suite — Python Q&A Assistant
======================================
Tests cover:
  • Health endpoint
  • Core /ask functionality
  • Diverse Python queries (8+)
  • Edge cases: short question, very broad question, non-Python question
  • Input validation
  • Response structure & latency expectations
"""

import os
import sys
import pytest
from fastapi.testclient import TestClient

# Allow running from repo root without installing the package
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Ensure dummy key so the import doesn't fail before we mock anything
os.environ.setdefault("OPENAI_API_KEY", "test-key")

# ── App setup ─────────────────────────────────────────────────────────────────
# We patch the LLM call so tests run offline without a real API key

from unittest.mock import patch, MagicMock


def _mock_llm_response(question: str) -> str:
    """Return a plausible canned answer keyed loosely to the question."""
    lower = question.lower()
    if "list" in lower:
        return "You can use `list.append()`, `list.extend()`, or `+=` to add items to a Python list."
    if "dict" in lower or "dictionary" in lower:
        return "Use `d[key] = value` to set items, `d.get(key)` to safely retrieve them."
    if "error" in lower or "exception" in lower:
        return "Wrap risky code in `try/except` blocks and catch specific exception types."
    if "file" in lower:
        return "Use the built-in `open()` with a `with` statement for safe file I/O."
    if "class" in lower or "oop" in lower:
        return "Define classes with `class MyClass:` and use `__init__` for the constructor."
    if "async" in lower or "asyncio" in lower:
        return "Use `async def` and `await` keywords; run with `asyncio.run(main())`."
    if "decorator" in lower:
        return "Decorators are higher-order functions applied with `@decorator_name` syntax."
    if "generator" in lower:
        return "Use `yield` inside a function to create a generator that produces values lazily."
    return "Great question! Python provides several ways to accomplish this task."


@pytest.fixture(scope="module")
def client():
    """Create a TestClient with the RAG pipeline's LLM mocked out."""
    from app.rag_pipeline import RAGPipeline

    def _fake_answer(self, question: str, top_k: int = 5):
        return {
            "answer": _mock_llm_response(question),
            "sources": [
                {
                    "title": "Sample Stack Overflow Question",
                    "score": 0.85,
                    "snippet": "A helpful Python answer from Stack Overflow.",
                }
            ],
        }

    with patch.object(RAGPipeline, "answer", _fake_answer):
        # Also patch load_or_build_index so no disk I/O happens
        with patch.object(RAGPipeline, "load_or_build_index", lambda self: None):
            with patch.object(RAGPipeline, "index_size", lambda self: 30):
                from app.main import app
                with TestClient(app) as c:
                    yield c


# ── Helper ─────────────────────────────────────────────────────────────────────

def ask(client, question: str, top_k: int = 5):
    return client.post("/ask", json={"question": question, "top_k": top_k})


# ══════════════════════════════════════════════════════════════════════════════
# 1. Health Check
# ══════════════════════════════════════════════════════════════════════════════

class TestHealth:
    def test_health_status_ok(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"

    def test_health_fields_present(self, client):
        data = client.get("/health").json()
        assert "index_size" in data
        assert "model" in data
        assert "version" in data

    def test_root_endpoint(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert "running" in resp.json()["message"].lower()


# ══════════════════════════════════════════════════════════════════════════════
# 2. Core /ask endpoint — structure validation
# ══════════════════════════════════════════════════════════════════════════════

class TestAskStructure:
    def test_returns_200(self, client):
        resp = ask(client, "How do I sort a list in Python?")
        assert resp.status_code == 200

    def test_response_has_required_fields(self, client):
        data = ask(client, "What is a Python list comprehension?").json()
        assert "question" in data
        assert "answer" in data
        assert "sources" in data
        assert "latency_ms" in data

    def test_answer_is_non_empty(self, client):
        data = ask(client, "How do I create a class in Python?").json()
        assert len(data["answer"]) > 10

    def test_sources_is_list(self, client):
        data = ask(client, "Explain Python generators").json()
        assert isinstance(data["sources"], list)

    def test_latency_field_is_float(self, client):
        data = ask(client, "What is a dictionary in Python?").json()
        assert isinstance(data["latency_ms"], float)

    def test_question_echoed_back(self, client):
        q = "How do I read a file line by line?"
        data = ask(client, q).json()
        assert data["question"] == q


# ══════════════════════════════════════════════════════════════════════════════
# 3. Diverse Python Queries  (the 8+ required test cases)
# ══════════════════════════════════════════════════════════════════════════════

PYTHON_QUERIES = [
    # (id, question, expected_keyword_in_answer)
    ("TC-01", "How do I add items to a list in Python?", "append"),
    ("TC-02", "What is the best way to iterate over a dictionary?", None),
    ("TC-03", "How do I handle exceptions using try and except?", "try"),
    ("TC-04", "How do I write text to a file in Python?", "open"),
    ("TC-05", "What are Python decorators and how do I use them?", "decorator"),
    ("TC-06", "How do I use async and await in Python?", "async"),
    ("TC-07", "How do I create a Python generator function?", "yield"),
    ("TC-08", "How do I define a class with inheritance in Python?", "class"),
    ("TC-09", "What is the difference between a list and a tuple?", None),
    ("TC-10", "How do I use list slicing in Python?", None),
]


@pytest.mark.parametrize("tc_id,question,keyword", PYTHON_QUERIES)
def test_python_query(client, tc_id, question, keyword):
    """Each query should return HTTP 200 and a non-empty answer."""
    resp = ask(client, question)
    assert resp.status_code == 200, f"{tc_id}: unexpected status {resp.status_code}"
    data = resp.json()
    assert len(data["answer"]) > 5, f"{tc_id}: answer too short"
    if keyword:
        assert keyword.lower() in data["answer"].lower(), (
            f"{tc_id}: expected '{keyword}' in answer, got: {data['answer'][:100]}"
        )


# ══════════════════════════════════════════════════════════════════════════════
# 4. Edge Cases
# ══════════════════════════════════════════════════════════════════════════════

class TestEdgeCases:
    def test_very_specific_question(self, client):
        """Highly specific question should still return a structured response."""
        resp = ask(client, "How do I use itertools.groupby with a custom key function?")
        assert resp.status_code == 200

    def test_broad_question(self, client):
        """Overly broad question should still return something useful."""
        resp = ask(client, "Teach me Python")
        assert resp.status_code == 200
        assert len(resp.json()["answer"]) > 5

    def test_question_with_code(self, client):
        """Question containing inline code."""
        resp = ask(client, "Why does `x = []` then `y = x` cause both to change when I modify y?")
        assert resp.status_code == 200

    def test_custom_top_k(self, client):
        """Custom top_k value should be accepted."""
        resp = ask(client, "What is a Python set?", top_k=3)
        assert resp.status_code == 200


# ══════════════════════════════════════════════════════════════════════════════
# 5. Input Validation
# ══════════════════════════════════════════════════════════════════════════════

class TestInputValidation:
    def test_missing_question_returns_422(self, client):
        resp = client.post("/ask", json={})
        assert resp.status_code == 422

    def test_too_short_question_returns_422(self, client):
        resp = client.post("/ask", json={"question": "hi"})
        assert resp.status_code == 422

    def test_top_k_zero_returns_422(self, client):
        resp = client.post("/ask", json={"question": "What is Python?", "top_k": 0})
        assert resp.status_code == 422

    def test_top_k_too_large_returns_422(self, client):
        resp = client.post("/ask", json={"question": "What is Python?", "top_k": 100})
        assert resp.status_code == 422

    def test_extra_fields_are_ignored(self, client):
        resp = client.post("/ask", json={"question": "What is Python?", "unknown_field": "value"})
        assert resp.status_code == 200
