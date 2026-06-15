# API Test Results — Python Q&A Assistant

**Date:** 2026-06-15  
**Dataset:** Stack Overflow Python Questions & Answers (Kaggle) — 50,000 top-scored Q&A pairs  
**Embedding model:** `all-MiniLM-L6-v2`  
**LLM:** `gpt-4o-mini`  
**Base URL:** `http://localhost:8000`

---

## Test Summary

| Category | Tests | Passed | Failed |
|---|---|---|---|
| Health & system | 3 | 3 | 0 |
| Response structure | 6 | 6 | 0 |
| Python query diversity | 10 | 10 | 0 |
| Edge cases | 4 | 4 | 0 |
| Input validation | 5 | 5 | 0 |
| **Total** | **28** | **28** | **0** |

```
pytest tests/test_api.py -v
======================== 28 passed in 9.29s ========================
```

---

## Diverse Query Results (TC-01 → TC-10)

### TC-01 — List operations
**Question:** `How do I add items to a list in Python?`

**Answer:**
> You can add items to a Python list using several methods:
>
> 1. **`append()`** – adds a single item to the end:
>    ```python
>    lst = [1, 2]
>    lst.append(3)   # [1, 2, 3]
>    ```
> 2. **`extend()`** – adds all items from another iterable:
>    ```python
>    lst.extend([4, 5])  # [1, 2, 3, 4, 5]
>    ```
> 3. **`insert(i, val)`** – inserts at a specific index.
> 4. **`+=`** operator – shorthand for extend.

**Top source:** "How to append to a list in Python?" — retrieval score: 0.921  
**Latency:** 742 ms  
**Observation:** ✅ Accurate, well-structured, code examples correct.

---

### TC-02 — Dictionary iteration
**Question:** `What is the best way to iterate over a dictionary?`

**Answer:**
> The idiomatic way is to iterate over `.items()` for key-value pairs:
> ```python
> for key, value in my_dict.items():
>     print(key, value)
> ```
> Use `.keys()` or `.values()` when you only need one side. In Python 3.7+ dictionaries maintain insertion order, so iteration order is predictable.

**Top source:** "How do I iterate over a dictionary in Python?" — score: 0.904  
**Latency:** 688 ms  
**Observation:** ✅ Correct modern Python answer. Mentions 3.7+ ordering guarantee — a common follow-up question.

---

### TC-03 — Exception handling
**Question:** `How do I handle exceptions using try and except?`

**Answer:**
> Wrap potentially failing code in a `try` block and catch specific exceptions:
> ```python
> try:
>     result = 10 / x
> except ZeroDivisionError:
>     print("Cannot divide by zero")
> except (TypeError, ValueError) as e:
>     print(f"Bad input: {e}")
> else:
>     print("Success:", result)
> finally:
>     print("Always runs")
> ```
> Avoid bare `except:` — always catch the most specific exception type possible.

**Top source:** "Python try/except, else, finally" — score: 0.898  
**Latency:** 801 ms  
**Observation:** ✅ Covers `else`/`finally` clauses which are often missed.

---

### TC-04 — File I/O
**Question:** `How do I write text to a file in Python?`

**Answer:**
> Use `open()` with the `'w'` mode inside a `with` statement to ensure the file is properly closed:
> ```python
> with open('output.txt', 'w') as f:
>     f.write('Hello, world!\n')
> ```
> To append instead of overwrite use `'a'`. For binary data use `'wb'`. The `with` statement guarantees the file is closed even if an exception occurs.

**Top source:** "How to write to a file in Python" — score: 0.917  
**Latency:** 656 ms  
**Observation:** ✅ Correctly emphasises `with` statement for resource safety.

---

### TC-05 — Decorators
**Question:** `What are Python decorators and how do I use them?`

**Answer:**
> A decorator is a function that takes another function and extends its behaviour without modifying it. Applied with the `@` syntax:
> ```python
> def my_decorator(func):
>     def wrapper(*args, **kwargs):
>         print("Before")
>         result = func(*args, **kwargs)
>         print("After")
>         return result
>     return wrapper
>
> @my_decorator
> def greet(name):
>     print(f"Hello, {name}")
> ```
> Common built-ins: `@staticmethod`, `@classmethod`, `@property`. `functools.wraps` preserves the original function's metadata.

**Top source:** "Understanding Python decorators" — score: 0.887  
**Latency:** 923 ms  
**Observation:** ✅ Solid conceptual + practical answer. Mention of `functools.wraps` is a nice touch.

---

### TC-06 — Async/await
**Question:** `How do I use async and await in Python?`

**Answer:**
> Use `async def` to define a coroutine and `await` to call it:
> ```python
> import asyncio
>
> async def fetch_data():
>     await asyncio.sleep(1)   # non-blocking wait
>     return "data"
>
> async def main():
>     result = await fetch_data()
>     print(result)
>
> asyncio.run(main())
> ```
> For HTTP, use `aiohttp` or `httpx` with async support. `asyncio.gather()` runs multiple coroutines concurrently.

**Top source:** "Python asyncio tutorial" — score: 0.876  
**Latency:** 871 ms  
**Observation:** ✅ Practical and up-to-date. `asyncio.run()` is the modern entry-point (Python 3.7+).

---

### TC-07 — Generators
**Question:** `How do I create a Python generator function?`

**Answer:**
> Replace `return` with `yield` inside a function:
> ```python
> def count_up(n):
>     for i in range(n):
>         yield i
>
> for val in count_up(5):
>     print(val)
> ```
> Generators are lazy — they produce values one at a time, saving memory for large sequences. Use `yield from` to delegate to another iterable. Generator expressions: `(x**2 for x in range(10))`.

**Top source:** "What does the yield keyword do?" — score: 0.911  
**Latency:** 745 ms  
**Observation:** ✅ Excellent. Correctly explains lazy evaluation. `yield from` is an advanced feature that earns bonus points.

---

### TC-08 — OOP / Inheritance
**Question:** `How do I define a class with inheritance in Python?`

**Answer:**
> Pass the parent class in parentheses and call `super().__init__()`:
> ```python
> class Animal:
>     def __init__(self, name):
>         self.name = name
>     def speak(self):
>         raise NotImplementedError
>
> class Dog(Animal):
>     def speak(self):
>         return f"{self.name} says Woof!"
>
> d = Dog("Rex")
> print(d.speak())   # Rex says Woof!
> ```
> Multiple inheritance is supported: `class C(A, B):`. Use `isinstance(obj, cls)` to check inheritance.

**Top source:** "Python class inheritance example" — score: 0.894  
**Latency:** 812 ms  
**Observation:** ✅ Clean example. Mentions `super()`, multiple inheritance, and `isinstance`.

---

### TC-09 — List vs Tuple
**Question:** `What is the difference between a list and a tuple?`

**Answer:**
> | | List | Tuple |
> |---|---|---|
> | Syntax | `[1, 2, 3]` | `(1, 2, 3)` |
> | Mutable | ✅ Yes | ❌ No |
> | Speed | Slower | Faster |
> | Use case | Data that changes | Fixed data, dict keys |
>
> Tuples are hashable (can be dict keys / set members). Lists cannot. Use tuples for things that shouldn't change, like coordinates or RGB values.

**Top source:** "Difference between list and tuple in Python" — score: 0.933  
**Latency:** 698 ms  
**Observation:** ✅ Well structured. The table format is a nice addition. Hashability point is correct and often tested.

---

### TC-10 — List slicing
**Question:** `How do I use list slicing in Python?`

**Answer:**
> Slicing syntax: `lst[start:stop:step]` — all parts optional.
> ```python
> lst = [0, 1, 2, 3, 4, 5]
> lst[1:4]    # [1, 2, 3]  — indices 1, 2, 3
> lst[:3]     # [0, 1, 2]  — first 3
> lst[::2]    # [0, 2, 4]  — every other element
> lst[::-1]   # [5, 4, 3, 2, 1, 0]  — reversed copy
> ```
> Slicing never raises `IndexError` — out-of-range indices are clamped. Slices create a new list (shallow copy).

**Top source:** "How slicing works in Python" — score: 0.919  
**Latency:** 704 ms  
**Observation:** ✅ Complete. The shallow-copy note is accurate and commonly misunderstood.

---

## Edge Cases Observed

| Case | Input | Outcome | Notes |
|---|---|---|---|
| Very specific | `itertools.groupby with custom key` | 200 OK, reasonable answer | Retrieval found partial matches; LLM filled gaps honestly |
| Broad question | `"Teach me Python"` | 200 OK, overview answer | LLM synthesised a high-level response from multiple context docs |
| Embedded code | `"Why does x = [] then y = x cause..."` | 200 OK | Special characters in question handled correctly |
| Non-Python adjacent | `"What is a REST API?"` | 200 OK, partial answer | Answered based on general knowledge; sources had lower relevance scores |

### Failure / Limitation Cases

| Case | Observation | Mitigation |
|---|---|---|
| Very niche / new library | Retrieval score < 0.5; LLM may hallucinate | Add confidence threshold; return "not enough context" below threshold |
| Typos in question | Embedding degrades gracefully; answer still useful | Consider a spellcheck pre-processing step |
| Question in non-English | Embedding model handles some multilingual; answers in English | Use `paraphrase-multilingual-MiniLM-L12-v2` for multilingual support |
| Very long question (800+ chars) | Still works, but retrieval focuses on first chunk | Truncate or summarise long questions before embedding |

---

## Performance Benchmarks

| Metric | Value |
|---|---|
| Avg retrieval latency | ~15 ms (FAISS in-memory) |
| Avg LLM latency | ~650 ms (gpt-4o-mini) |
| Avg total `/ask` latency | ~750 ms |
| Index build time (50k docs) | ~4 min (embedding) |
| Index size on disk | ~120 MB (FAISS) + 45 MB (docs.pkl) |
| Throughput (single worker) | ~80 req/min |
