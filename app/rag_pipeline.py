"""
RAG Pipeline
------------
1. Load & pre-process Stack Overflow Python Q&A CSV files
2. Index documents with BM25 (keyword) + TF-IDF (semantic-ish) — fully local, no model download
3. Persist index to disk for fast restarts
4. Use Groq LLM (free, fast) to generate grounded answers
"""

import os
import logging
import pickle
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI

logger = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────

DATA_DIR  = Path(os.getenv("DATA_DIR",  "data"))
INDEX_DIR = Path(os.getenv("INDEX_DIR", "index"))

# Groq — free, OpenAI-compatible
LLM_MODEL       = os.getenv("LLM_MODEL",       "llama-3.3-70b-versatile")
GROQ_API_KEY    = os.getenv("GROQ_API_KEY",    "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.groq.com/openai/v1")

SYSTEM_PROMPT = """You are a helpful Python programming assistant.
Answer questions about Python using the provided Stack Overflow context.
Be accurate and concise. Format code with markdown code blocks (```python).
If the context doesn't fully cover the question, say so but still help."""


def _truncate(text: str, n: int = 500) -> str:
    return text[:n] + "…" if len(text) > n else text


def _tokenize(text: str) -> list[str]:
    """Simple whitespace+punctuation tokenizer for BM25."""
    import re
    return re.findall(r"[a-z0-9]+", text.lower())


# ── Pipeline ──────────────────────────────────────────────────────────────────

class RAGPipeline:
    """Hybrid BM25 + TF-IDF retrieval with Groq LLM generation."""

    def __init__(self):
        self.llm_model_name = LLM_MODEL
        self._docs: list[dict] = []
        self._bm25: BM25Okapi | None = None
        self._tfidf: TfidfVectorizer | None = None
        self._tfidf_matrix = None
        self._llm: OpenAI | None = None

    @property
    def llm(self) -> OpenAI:
        if self._llm is None:
            self._llm = OpenAI(api_key=GROQ_API_KEY, base_url=OPENAI_BASE_URL)
        return self._llm

    # ── Index build / load ────────────────────────────────────────────────────

    def load_or_build_index(self):
        index_path = INDEX_DIR / "bm25.pkl"
        if index_path.exists():
            logger.info("Loading existing index from %s", INDEX_DIR)
            with open(index_path, "rb") as f:
                saved = pickle.load(f)
            self._docs        = saved["docs"]
            self._bm25        = saved["bm25"]
            self._tfidf       = saved["tfidf"]
            self._tfidf_matrix = saved["tfidf_matrix"]
            logger.info("Loaded %d documents.", len(self._docs))
        else:
            logger.info("Building index from raw data…")
            self._build_index()

    def _load_dataset(self) -> pd.DataFrame:
        q_path = DATA_DIR / "Questions.csv"
        a_path = DATA_DIR / "Answers.csv"
        if q_path.exists() and a_path.exists():
            logger.info("Loading Stack Overflow dataset…")
            questions = pd.read_csv(q_path, encoding="latin-1", low_memory=False)
            answers   = pd.read_csv(a_path, encoding="latin-1", low_memory=False)
            top_ans = (
                answers.sort_values("Score", ascending=False)
                       .groupby("ParentId").first().reset_index()
                       .rename(columns={"ParentId": "QuestionId",
                                        "Body": "AnswerBody",
                                        "Score": "AnswerScore"})
            )
            merged = questions.merge(
                top_ans[["QuestionId", "AnswerBody", "AnswerScore"]],
                left_on="Id", right_on="QuestionId", how="inner"
            )
            max_rows = int(os.getenv("MAX_DOCS", "50000"))
            return merged.nlargest(max_rows, "Score")
        else:
            logger.warning("Dataset not found — using built-in sample (30 rows).")
            return self._sample_data()

    def _sample_data(self) -> pd.DataFrame:
        samples = [
            ("How do I read a CSV file in Python?",
             "Use pandas:\n```python\nimport pandas as pd\ndf = pd.read_csv('file.csv')\nprint(df.head())\n```\nOr the built-in `csv` module for simple cases."),
            ("How do I reverse a list in Python?",
             "Three ways:\n```python\nlst = [1,2,3]\nlst[::-1]        # new reversed list\nlist(reversed(lst))  # iterator\nlst.reverse()    # in-place\n```"),
            ("What is a lambda function?",
             "An anonymous inline function:\n```python\nsquare = lambda x: x**2\nprint(square(4))  # 16\n```\nUseful as short callbacks for `map()`, `filter()`, `sorted()`."),
            ("How do I handle exceptions in Python?",
             "```python\ntry:\n    result = 10 / x\nexcept ZeroDivisionError:\n    print('Cannot divide by zero')\nexcept (TypeError, ValueError) as e:\n    print(f'Bad input: {e}')\nelse:\n    print('Success:', result)\nfinally:\n    print('Always runs')\n```"),
            ("How do I merge two dictionaries?",
             "Python 3.9+: `merged = d1 | d2`\nEarlier versions: `merged = {**d1, **d2}`\nOr: `d1.update(d2)` (modifies d1 in-place)."),
            ("How do I sort a list of tuples by the second element?",
             "```python\nlst = [('b',2), ('a',1), ('c',3)]\nsorted(lst, key=lambda x: x[1])  # [('a',1),('b',2),('c',3)]\n```"),
            ("What is the difference between a list and a tuple?",
             "Lists are mutable (`[]`), tuples are immutable (`()`). Tuples are faster and hashable (can be dict keys). Use tuples for fixed data like coordinates."),
            ("How do I check if a key exists in a dictionary?",
             "`if key in my_dict:` — O(1) average. Use `dict.get(key, default)` to avoid KeyError and supply a fallback."),
            ("How do I concatenate strings in Python?",
             "Prefer f-strings: `f'{a}{b}'`. For many strings: `''.join(parts)`. The `+` operator is fine for a few strings."),
            ("How do I install a Python package?",
             "`pip install package_name`. Inside a virtual env: `python -m venv venv && source venv/bin/activate && pip install package`."),
            ("What is list comprehension in Python?",
             "```python\n# [expression for item in iterable if condition]\nsquares = [x**2 for x in range(10) if x % 2 == 0]\n```\nFaster and more Pythonic than equivalent for-loops."),
            ("How do I write to a file in Python?",
             "```python\nwith open('file.txt', 'w') as f:\n    f.write('hello\\n')\n    f.writelines(['line1\\n', 'line2\\n'])\n```\nThe `with` statement ensures the file is closed even on error."),
            ("How do I use enumerate in Python?",
             "```python\nfor i, val in enumerate(['a','b','c'], start=1):\n    print(i, val)  # 1 a, 2 b, 3 c\n```\nAvoid manual index counters."),
            ("What is the difference between == and is?",
             "`==` checks value equality. `is` checks identity (same object in memory). Use `is` only for `None`, `True`, `False` — never for strings or numbers."),
            ("How do I flatten a nested list?",
             "```python\nimport itertools\nnested = [[1,2],[3,4],[5]]\nflat = list(itertools.chain.from_iterable(nested))\n# or: [x for sub in nested for x in sub]\n```"),
            ("How do I use *args and **kwargs?",
             "```python\ndef func(*args, **kwargs):\n    print(args)   # tuple of positional args\n    print(kwargs) # dict of keyword args\nfunc(1,2, name='Alice')  # (1,2)  {'name':'Alice'}\n```"),
            ("What are Python decorators?",
             "```python\nimport functools\ndef my_decorator(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        print('Before')\n        result = func(*args, **kwargs)\n        print('After')\n        return result\n    return wrapper\n\n@my_decorator\ndef greet(): print('Hello')\n```"),
            ("How do I use context managers?",
             "`with` statement calls `__enter__` and `__exit__` automatically:\n```python\nwith open('f') as f:\n    data = f.read()\n# file auto-closed here\n```\nCreate custom ones with `contextlib.contextmanager`."),
            ("How do I profile Python code?",
             "`python -m cProfile -s cumtime script.py` for function-level profiling. `timeit` for micro-benchmarks:\n```python\nimport timeit\ntimeit.timeit('x**2', number=1_000_000)\n```"),
            ("How do I use regular expressions in Python?",
             "```python\nimport re\npattern = re.compile(r'\\d+')\nmatches = pattern.findall('abc 123 def 456')  # ['123', '456']\nre.sub(r'\\s+', ' ', text)  # replace whitespace\n```"),
            ("How do I make HTTP requests in Python?",
             "```python\nimport requests\nresp = requests.get('https://api.example.com/data', timeout=5)\nresp.raise_for_status()  # raise on 4xx/5xx\ndata = resp.json()\n```"),
            ("How do I use asyncio?",
             "```python\nimport asyncio\nasync def fetch():\n    await asyncio.sleep(1)\n    return 'done'\nasync def main():\n    results = await asyncio.gather(fetch(), fetch())\n    print(results)\nasyncio.run(main())\n```"),
            ("What are Python generators?",
             "```python\ndef infinite_counter(start=0):\n    while True:\n        yield start\n        start += 1\ng = infinite_counter()\nnext(g), next(g)  # 0, 1\n```\nLazy — produce values on demand, saving memory."),
            ("How do I deepcopy an object?",
             "```python\nimport copy\noriginal = {'a': [1,2,3]}\nclone = copy.deepcopy(original)\nclone['a'].append(4)\nprint(original)  # {'a': [1,2,3]} — unaffected\n```"),
            ("How do I format floats in Python?",
             "f-string: `f'{value:.2f}'` — 2 decimal places. `f'{value:,.2f}'` — with thousands separator. `f'{value:.2%}'` — as percentage."),
            ("How do I count occurrences in a list?",
             "```python\nfrom collections import Counter\nc = Counter(['a','b','a','c','a'])\nc.most_common(2)  # [('a',3),('b',1)]\n```"),
            ("How do I use type hints?",
             "```python\nfrom typing import Optional, List\ndef greet(name: str, times: int = 1) -> str:\n    return (name + ' ') * times\ndef process(items: List[int]) -> Optional[int]:\n    return items[0] if items else None\n```"),
            ("How do I use dataclasses?",
             "```python\nfrom dataclasses import dataclass, field\n@dataclass\nclass Point:\n    x: float\n    y: float\n    tags: list = field(default_factory=list)\n    def distance(self): return (self.x**2 + self.y**2)**0.5\n```"),
            ("How do I use pathlib?",
             "```python\nfrom pathlib import Path\np = Path('data') / 'file.txt'\np.write_text('hello')\ntext = p.read_text()\nfor f in Path('.').glob('*.py'): print(f)\n```"),
            ("How do I create a class with inheritance in Python?",
             "```python\nclass Animal:\n    def __init__(self, name): self.name = name\n    def speak(self): raise NotImplementedError\nclass Dog(Animal):\n    def speak(self): return f'{self.name}: Woof!'\nd = Dog('Rex')\nprint(d.speak())  # Rex: Woof!\nprint(isinstance(d, Animal))  # True\n```"),
        ]
        rows = [{"Title": q, "AnswerBody": a, "Score": 100-i} for i,(q,a) in enumerate(samples)]
        return pd.DataFrame(rows)

    def _build_index(self):
        df = self._load_dataset()
        docs, tokenized = [], []
        for _, row in df.iterrows():
            title  = str(row.get("Title", "")).strip()
            body   = str(row.get("Body", "")).strip()
            answer = str(row.get("AnswerBody", "")).strip()
            score  = int(row.get("Score", 0))
            q_text = title + (" " + body[:300] if body and body != "nan" else "")
            combined = f"{q_text} {answer[:400]}"
            docs.append({"title": title, "answer": answer, "score": score, "combined": combined})
            tokenized.append(_tokenize(combined))

        logger.info("Building BM25 index over %d docs…", len(docs))
        bm25 = BM25Okapi(tokenized)

        logger.info("Building TF-IDF matrix…")
        tfidf = TfidfVectorizer(max_features=30_000, ngram_range=(1, 2))
        tfidf_matrix = tfidf.fit_transform([d["combined"] for d in docs])

        self._docs = docs
        self._bm25 = bm25
        self._tfidf = tfidf
        self._tfidf_matrix = tfidf_matrix

        INDEX_DIR.mkdir(parents=True, exist_ok=True)
        with open(INDEX_DIR / "bm25.pkl", "wb") as f:
            pickle.dump({"docs": docs, "bm25": bm25,
                         "tfidf": tfidf, "tfidf_matrix": tfidf_matrix}, f)
        logger.info("Index saved — %d docs.", len(docs))

    # ── Retrieval ─────────────────────────────────────────────────────────────

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        """Hybrid BM25 + TF-IDF retrieval with score fusion."""
        n = len(self._docs)

        # BM25 scores (normalised)
        bm25_scores = np.array(self._bm25.get_scores(_tokenize(query)))
        bm25_norm   = bm25_scores / (bm25_scores.max() + 1e-9)

        # TF-IDF cosine scores
        q_vec       = self._tfidf.transform([query])
        tfidf_scores = cosine_similarity(q_vec, self._tfidf_matrix).flatten()

        # Hybrid: 50% BM25 + 50% TF-IDF
        fused = 0.5 * bm25_norm + 0.5 * tfidf_scores
        top_idx = np.argsort(fused)[::-1][:top_k]

        results = []
        for idx in top_idx:
            doc = self._docs[idx].copy()
            doc["retrieval_score"] = float(fused[idx])
            results.append(doc)
        return results

    def _build_context(self, docs: list[dict]) -> str:
        parts = []
        for i, doc in enumerate(docs, 1):
            parts.append(
                f"[Source {i}] {doc['title']}\n"
                f"{_truncate(doc['answer'], 500)}"
            )
        return "\n\n---\n\n".join(parts)

    def answer(self, question: str, top_k: int = 5) -> dict[str, Any]:
        docs    = self.retrieve(question, top_k=top_k)
        context = self._build_context(docs)
        user_msg = (
            f"Context from Stack Overflow:\n\n{context}\n\n"
            f"Question: {question}\n\n"
            "Provide a clear, accurate Python answer based on the context above."
        )
        resp = self.llm.chat.completions.create(
            model=self.llm_model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_msg},
            ],
            temperature=0.2,
            max_tokens=800,
        )
        answer_text = resp.choices[0].message.content.strip()
        sources = [
            {"title": d["title"],
             "score": round(d["retrieval_score"], 4),
             "snippet": _truncate(d["answer"], 200)}
            for d in docs
        ]
        return {"answer": answer_text, "sources": sources}

    def index_size(self) -> int:
        return len(self._docs)
