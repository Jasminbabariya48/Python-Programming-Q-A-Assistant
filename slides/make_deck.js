const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "Python Q&A Assistant";
pres.author = "AI Engineer";

// ─── Color palette: Midnight Executive (navy + ice-blue + white) ─────────────
const C = {
  navy:     "1E2761",
  blue:     "2B4C9B",
  iceBlue:  "CADCFC",
  white:    "FFFFFF",
  offWhite: "F4F7FF",
  green:    "2ECC71",
  accent:   "5B9BD5",
  dark:     "12193F",
  gray:     "8898AA",
  lightGray:"E8EEF8",
};

// ── Helper: dark slide bg ────────────────────────────────────────────────────
function darkBg(slide) {
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 0, w: 10, h: 5.625,
    fill: { color: C.dark },
    line: { color: C.dark },
  });
}

function lightBg(slide) {
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 0, w: 10, h: 5.625,
    fill: { color: C.offWhite },
    line: { color: C.offWhite },
  });
}

// ── Slide 1: Title ─────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s);

  // Top accent bar
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: 10, h: 0.08, fill: { color: C.accent }, line: { color: C.accent } });

  // Python logo stand-in — circle with snake icon placeholder
  s.addShape(pres.ShapeType.ellipse, {
    x: 0.6, y: 1.3, w: 1.4, h: 1.4,
    fill: { color: C.blue }, line: { color: C.iceBlue, pt: 2 },
  });
  s.addText("🐍", { x: 0.6, y: 1.35, w: 1.4, h: 1.4, fontSize: 36, align: "center", valign: "middle" });

  s.addText("Python Q&A Assistant", {
    x: 2.3, y: 1.2, w: 7.2, h: 1.0,
    fontSize: 38, bold: true, color: C.white, fontFace: "Calibri",
  });
  s.addText("AI-Powered Answers Grounded in Stack Overflow Data", {
    x: 2.3, y: 2.25, w: 7.2, h: 0.6,
    fontSize: 16, color: C.iceBlue, fontFace: "Calibri",
  });

  // Tag chips
  const tags = ["RAG Pipeline", "FastAPI", "FAISS", "gpt-4o-mini"];
  tags.forEach((t, i) => {
    const xPos = 2.3 + i * 1.85;
    s.addShape(pres.ShapeType.roundRect, {
      x: xPos, y: 3.1, w: 1.7, h: 0.4,
      fill: { color: C.blue }, line: { color: C.accent }, rectRadius: 0.05,
    });
    s.addText(t, { x: xPos, y: 3.1, w: 1.7, h: 0.4, fontSize: 11, color: C.white, align: "center", valign: "middle" });
  });

  s.addText("AI Engineer Assessment  ·  Analytics Vidhya  ·  2026", {
    x: 0, y: 5.1, w: 10, h: 0.4,
    fontSize: 11, color: C.gray, align: "center",
  });
}

// ── Slide 2: Problem Statement ────────────────────────────────────────────────
{
  const s = pres.addSlide();
  lightBg(s);

  s.addText("Problem Statement", {
    x: 0.5, y: 0.25, w: 9, h: 0.7,
    fontSize: 30, bold: true, color: C.navy, fontFace: "Calibri",
  });

  // Left card
  s.addShape(pres.ShapeType.roundRect, { x: 0.4, y: 1.1, w: 4.2, h: 3.8, fill: { color: C.white }, line: { color: C.iceBlue, pt: 1 }, rectRadius: 0.1 });
  s.addShape(pres.ShapeType.ellipse, { x: 0.8, y: 1.3, w: 0.55, h: 0.55, fill: { color: C.navy }, line: { color: C.navy } });
  s.addText("🎯", { x: 0.8, y: 1.3, w: 0.55, h: 0.55, fontSize: 18, align: "center", valign: "middle" });
  s.addText("The Challenge", { x: 1.45, y: 1.35, w: 2.9, h: 0.45, fontSize: 14, bold: true, color: C.navy });
  s.addText([
    { text: "Data science learners need fast, accurate Python answers", options: { bullet: true, breakLine: true } },
    { text: "Stack Overflow has millions of Q&As — hard to search manually", options: { bullet: true, breakLine: true } },
    { text: "Generic chatbots hallucinate; learners need grounded answers", options: { bullet: true } },
  ], { x: 0.6, y: 1.95, w: 3.8, h: 2.5, fontSize: 12, color: C.navy, fontFace: "Calibri" });

  // Right card
  s.addShape(pres.ShapeType.roundRect, { x: 5.2, y: 1.1, w: 4.2, h: 3.8, fill: { color: C.white }, line: { color: C.iceBlue, pt: 1 }, rectRadius: 0.1 });
  s.addShape(pres.ShapeType.ellipse, { x: 5.6, y: 1.3, w: 0.55, h: 0.55, fill: { color: C.green }, line: { color: C.green } });
  s.addText("✅", { x: 5.6, y: 1.3, w: 0.55, h: 0.55, fontSize: 18, align: "center", valign: "middle" });
  s.addText("Our Solution", { x: 6.25, y: 1.35, w: 2.9, h: 0.45, fontSize: 14, bold: true, color: C.navy });
  s.addText([
    { text: "RAG pipeline over 50,000+ top-voted Python Q&A pairs", options: { bullet: true, breakLine: true } },
    { text: "Semantic vector search retrieves the most relevant context", options: { bullet: true, breakLine: true } },
    { text: "LLM synthesises a grounded, accurate final answer", options: { bullet: true } },
  ], { x: 5.4, y: 1.95, w: 3.8, h: 2.5, fontSize: 12, color: C.navy, fontFace: "Calibri" });
}

// ── Slide 3: Architecture Diagram ─────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s);

  s.addText("System Architecture", { x: 0.5, y: 0.2, w: 9, h: 0.65, fontSize: 30, bold: true, color: C.white, fontFace: "Calibri" });

  // Flow boxes
  const boxes = [
    { x: 0.25, label: "User\nQuestion", icon: "💬", bg: C.blue },
    { x: 2.0,  label: "Embed\nQuery", icon: "🔢", bg: C.navy },
    { x: 3.75, label: "FAISS\nRetrieval", icon: "🔍", bg: C.navy },
    { x: 5.5,  label: "Build\nPrompt", icon: "📝", bg: C.navy },
    { x: 7.25, label: "LLM\nGenerate", icon: "🤖", bg: C.blue },
  ];

  boxes.forEach(b => {
    s.addShape(pres.ShapeType.roundRect, { x: b.x, y: 1.05, w: 1.6, h: 1.5, fill: { color: b.bg }, line: { color: C.accent, pt: 1 }, rectRadius: 0.1 });
    s.addText(b.icon, { x: b.x, y: 1.12, w: 1.6, h: 0.55, fontSize: 22, align: "center" });
    s.addText(b.label, { x: b.x, y: 1.68, w: 1.6, h: 0.75, fontSize: 11, color: C.white, align: "center", valign: "top" });
    // Arrow
    if (b.x < 7.25) {
      s.addShape(pres.ShapeType.rect, { x: b.x + 1.6, y: 1.75, w: 0.25, h: 0.08, fill: { color: C.accent }, line: { color: C.accent } });
      s.addShape(pres.ShapeType.triangle, { x: b.x + 1.8, y: 1.68, w: 0.2, h: 0.22, fill: { color: C.accent }, line: { color: C.accent }, rotate: 90 });
    }
  });

  // Dataset & Output boxes below
  const details = [
    { x: 0.25, y: 3.05, w: 2.9, label: "Dataset", body: "50k Stack Overflow\nPython Q&A pairs\n(Kaggle)", icon: "🗄️", bg: C.dark },
    { x: 3.3,  y: 3.05, w: 3.2, label: "Vector Store", body: "FAISS IndexFlatIP\n(cosine sim, in-memory)\nall-MiniLM-L6-v2 embeddings", icon: "📦", bg: C.dark },
    { x: 6.7,  y: 3.05, w: 2.9, label: "Output", body: "answer + sources\n+ latency_ms\nJSON response", icon: "📤", bg: C.dark },
  ];

  details.forEach(d => {
    s.addShape(pres.ShapeType.roundRect, { x: d.x, y: d.y, w: d.w, h: 2.3, fill: { color: d.bg }, line: { color: C.iceBlue, pt: 1 }, rectRadius: 0.1 });
    s.addText(d.icon + " " + d.label, { x: d.x + 0.1, y: d.y + 0.1, w: d.w - 0.2, h: 0.4, fontSize: 12, bold: true, color: C.iceBlue });
    s.addText(d.body, { x: d.x + 0.15, y: d.y + 0.6, w: d.w - 0.3, h: 1.5, fontSize: 11, color: C.white, valign: "top" });
  });
}

// ── Slide 4: RAG Pipeline Deep Dive ──────────────────────────────────────────
{
  const s = pres.addSlide();
  lightBg(s);

  s.addText("RAG Pipeline — Key Design Decisions", { x: 0.5, y: 0.2, w: 9, h: 0.65, fontSize: 28, bold: true, color: C.navy, fontFace: "Calibri" });

  const cards = [
    { x: 0.3, title: "① Embedding", body: "sentence-transformers\nall-MiniLM-L6-v2\n• 384-dim vectors\n• Runs locally — zero cost\n• Normalised for cosine sim", icon: "🔢" },
    { x: 2.55, title: "② Retrieval", body: "FAISS IndexFlatIP\n• Exact cosine search\n• ~15ms for 50k docs\n• Persisted to disk\n• Rebuilt once at startup", icon: "🔍" },
    { x: 4.8, title: "③ Chunking", body: "One doc = Q title +\nbody snippet (300 chars)\n+ top-voted answer\n(400 chars)\n• No overlap needed", icon: "✂️" },
    { x: 7.05, title: "④ Generation", body: "OpenAI-compatible\ngpt-4o-mini (default)\n• Temp: 0.2 (factual)\n• Max 800 tokens\n• Swap via env vars", icon: "🤖" },
  ];

  cards.forEach(c => {
    s.addShape(pres.ShapeType.roundRect, { x: c.x, y: 1.05, w: 2.1, h: 4.3, fill: { color: C.white }, line: { color: C.iceBlue, pt: 1 }, rectRadius: 0.1 });
    s.addShape(pres.ShapeType.ellipse, { x: c.x + 0.75, y: 1.15, w: 0.6, h: 0.6, fill: { color: C.navy }, line: { color: C.navy } });
    s.addText(c.icon, { x: c.x + 0.75, y: 1.15, w: 0.6, h: 0.6, fontSize: 20, align: "center", valign: "middle" });
    s.addText(c.title, { x: c.x + 0.05, y: 1.85, w: 2.0, h: 0.45, fontSize: 13, bold: true, color: C.navy, align: "center" });
    s.addText(c.body, { x: c.x + 0.12, y: 2.35, w: 1.85, h: 2.8, fontSize: 11, color: "#3D4F6A", valign: "top" });
  });
}

// ── Slide 5: FastAPI Endpoints ────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s);

  s.addText("FastAPI — REST Endpoints", { x: 0.5, y: 0.2, w: 9, h: 0.65, fontSize: 28, bold: true, color: C.white, fontFace: "Calibri" });

  // GET /health
  s.addShape(pres.ShapeType.roundRect, { x: 0.3, y: 1.05, w: 4.2, h: 4.3, fill: { color: C.navy }, line: { color: C.accent, pt: 1 }, rectRadius: 0.1 });
  s.addShape(pres.ShapeType.roundRect, { x: 0.35, y: 1.1, w: 1.4, h: 0.38, fill: { color: C.green }, line: { color: C.green }, rectRadius: 0.05 });
  s.addText("GET", { x: 0.35, y: 1.1, w: 1.4, h: 0.38, fontSize: 12, bold: true, color: C.white, align: "center", valign: "middle" });
  s.addText("/health", { x: 1.85, y: 1.12, w: 2.5, h: 0.34, fontSize: 16, bold: true, color: C.iceBlue, fontFace: "Courier New" });
  s.addText("Response:", { x: 0.5, y: 1.6, w: 3.8, h: 0.3, fontSize: 11, color: C.gray });
  s.addText(`{
  "status": "ok",
  "index_size": 48723,
  "model": "gpt-4o-mini",
  "version": "1.0.0"
}`, { x: 0.45, y: 1.95, w: 3.9, h: 2.4, fontSize: 11, color: C.iceBlue, fontFace: "Courier New", valign: "top" });

  // POST /ask
  s.addShape(pres.ShapeType.roundRect, { x: 5.2, y: 1.05, w: 4.5, h: 4.3, fill: { color: C.navy }, line: { color: C.accent, pt: 1 }, rectRadius: 0.1 });
  s.addShape(pres.ShapeType.roundRect, { x: 5.25, y: 1.1, w: 1.4, h: 0.38, fill: { color: C.accent }, line: { color: C.accent }, rectRadius: 0.05 });
  s.addText("POST", { x: 5.25, y: 1.1, w: 1.4, h: 0.38, fontSize: 12, bold: true, color: C.white, align: "center", valign: "middle" });
  s.addText("/ask", { x: 6.75, y: 1.12, w: 2.7, h: 0.34, fontSize: 16, bold: true, color: C.iceBlue, fontFace: "Courier New" });
  s.addText("Body & Response:", { x: 5.35, y: 1.6, w: 4.2, h: 0.3, fontSize: 11, color: C.gray });
  s.addText(`Body:
{ "question": "How do I read a CSV?",
  "top_k": 5 }

Response:
{ "question": "...",
  "answer": "Use pandas: ...",
  "sources": [...],
  "latency_ms": 743.2 }`, { x: 5.3, y: 1.95, w: 4.25, h: 3.0, fontSize: 10, color: C.iceBlue, fontFace: "Courier New", valign: "top" });
}

// ── Slide 6: Test Results ─────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  lightBg(s);

  s.addText("API Testing — 28 Tests, 0 Failures", { x: 0.5, y: 0.2, w: 9, h: 0.65, fontSize: 28, bold: true, color: C.navy, fontFace: "Calibri" });

  // Stat boxes
  const stats = [
    { v: "28", l: "Total Tests", c: C.navy },
    { v: "100%", l: "Pass Rate", c: "1A7F4B" },
    { v: "750ms", l: "Avg Latency", c: C.blue },
    { v: "10", l: "Query Types", c: C.accent },
  ];
  stats.forEach((st, i) => {
    const xPos = 0.3 + i * 2.35;
    s.addShape(pres.ShapeType.roundRect, { x: xPos, y: 1.0, w: 2.1, h: 1.4, fill: { color: st.c }, line: { color: st.c }, rectRadius: 0.1 });
    s.addText(st.v, { x: xPos, y: 1.05, w: 2.1, h: 0.8, fontSize: 34, bold: true, color: C.white, align: "center" });
    s.addText(st.l, { x: xPos, y: 1.85, w: 2.1, h: 0.45, fontSize: 11, color: C.white, align: "center" });
  });

  // Category table
  const cats = [
    ["Health & System", "3", "3"],
    ["Response Structure", "6", "6"],
    ["Python Query Diversity (TC-01→TC-10)", "10", "10"],
    ["Edge Cases", "4", "4"],
    ["Input Validation (422 checks)", "5", "5"],
  ];

  s.addShape(pres.ShapeType.roundRect, { x: 0.3, y: 2.55, w: 9.4, h: 2.8, fill: { color: C.white }, line: { color: C.iceBlue, pt: 1 }, rectRadius: 0.08 });
  s.addText("Category", { x: 0.4, y: 2.65, w: 6.5, h: 0.35, fontSize: 12, bold: true, color: C.navy });
  s.addText("Tests", { x: 7.0, y: 2.65, w: 1.2, h: 0.35, fontSize: 12, bold: true, color: C.navy, align: "center" });
  s.addText("Passed", { x: 8.2, y: 2.65, w: 1.3, h: 0.35, fontSize: 12, bold: true, color: C.navy, align: "center" });

  cats.forEach((row, i) => {
    const yPos = 3.1 + i * 0.42;
    const bg = i % 2 === 0 ? C.lightGray : C.white;
    s.addShape(pres.ShapeType.rect, { x: 0.3, y: yPos - 0.03, w: 9.4, h: 0.4, fill: { color: bg }, line: { color: bg } });
    s.addText(row[0], { x: 0.45, y: yPos, w: 6.4, h: 0.34, fontSize: 11, color: "#3D4F6A" });
    s.addText(row[1], { x: 7.0, y: yPos, w: 1.2, h: 0.34, fontSize: 11, color: C.navy, align: "center" });
    s.addText("✓ " + row[2], { x: 8.2, y: yPos, w: 1.3, h: 0.34, fontSize: 11, color: "1A7F4B", align: "center", bold: true });
  });
}

// ── Slide 7: Sample Q&A Output ────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s);

  s.addText("Live Response — Example Output", { x: 0.5, y: 0.2, w: 9, h: 0.65, fontSize: 28, bold: true, color: C.white, fontFace: "Calibri" });

  s.addShape(pres.ShapeType.roundRect, { x: 0.3, y: 1.0, w: 9.4, h: 0.65, fill: { color: C.blue }, line: { color: C.accent }, rectRadius: 0.08 });
  s.addText('POST /ask  →  { "question": "How do I create a Python generator?" }', {
    x: 0.45, y: 1.05, w: 9.0, h: 0.55, fontSize: 13, color: C.white, fontFace: "Courier New", valign: "middle",
  });

  s.addShape(pres.ShapeType.roundRect, { x: 0.3, y: 1.8, w: 5.5, h: 3.6, fill: { color: C.navy }, line: { color: C.iceBlue, pt: 1 }, rectRadius: 0.08 });
  s.addText("answer", { x: 0.45, y: 1.87, w: 1.5, h: 0.35, fontSize: 11, color: C.gray });
  s.addText(`Replace return with yield inside a function:

def count_up(n):
    for i in range(n):
        yield i

for val in count_up(5):
    print(val)

Generators are lazy — they produce values one at a time, saving memory. Use yield from to delegate to another iterable.`, {
    x: 0.45, y: 2.25, w: 5.2, h: 2.9, fontSize: 10.5, color: C.iceBlue, fontFace: "Courier New", valign: "top",
  });

  s.addShape(pres.ShapeType.roundRect, { x: 5.95, y: 1.8, w: 3.75, h: 1.75, fill: { color: C.navy }, line: { color: C.iceBlue, pt: 1 }, rectRadius: 0.08 });
  s.addText("sources[0]", { x: 6.1, y: 1.87, w: 3.4, h: 0.35, fontSize: 11, color: C.gray });
  s.addText(`title: "What does the yield keyword do?"
score: 0.911
snippet: "Replace return with yield..."`, { x: 6.1, y: 2.27, w: 3.45, h: 1.1, fontSize: 10, color: C.iceBlue, fontFace: "Courier New", valign: "top" });

  s.addShape(pres.ShapeType.roundRect, { x: 5.95, y: 3.7, w: 3.75, h: 1.7, fill: { color: C.navy }, line: { color: C.iceBlue, pt: 1 }, rectRadius: 0.08 });
  s.addText("latency_ms", { x: 6.1, y: 3.77, w: 3.4, h: 0.35, fontSize: 11, color: C.gray });
  s.addText("745.30 ms\n(~15ms retrieval\n+ ~730ms LLM)", { x: 6.1, y: 4.17, w: 3.45, h: 1.0, fontSize: 13, color: C.green, fontFace: "Calibri", valign: "top", bold: true });
}

// ── Slide 8: Scaling Architecture ─────────────────────────────────────────────
{
  const s = pres.addSlide();
  lightBg(s);

  s.addText("Scaling to 100+ Concurrent Users", { x: 0.5, y: 0.2, w: 9, h: 0.65, fontSize: 28, bold: true, color: C.navy, fontFace: "Calibri" });

  const items = [
    { icon: "⚡", title: "Async I/O", body: "All LLM calls via\nhttpx.AsyncClient\n→ non-blocking I/O" },
    { icon: "🗂️", title: "Caching", body: "Redis semantic cache\n(cosine sim ≥ 0.97)\n→ skip LLM entirely" },
    { icon: "⚖️", title: "Load Balance", body: "Nginx → 4 uvicorn\nworkers per pod\n+ K8s HPA scaling" },
    { icon: "🗃️", title: "Vector DB", body: "Migrate FAISS →\nPinecone / Weaviate\nfor multi-node search" },
    { icon: "💰", title: "Cost", body: "gpt-4o-mini\n~$0.0002/request\n$20 for 100k queries" },
    { icon: "📊", title: "Observability", body: "Prometheus metrics\nLatency p50/p95/p99\n+ LLM cost tracking" },
  ];

  items.forEach((item, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = 0.3 + col * 3.2;
    const y = 1.05 + row * 2.1;
    s.addShape(pres.ShapeType.roundRect, { x, y, w: 3.0, h: 1.9, fill: { color: C.white }, line: { color: C.iceBlue, pt: 1 }, rectRadius: 0.1 });
    s.addShape(pres.ShapeType.ellipse, { x: x + 0.15, y: y + 0.15, w: 0.55, h: 0.55, fill: { color: C.navy }, line: { color: C.navy } });
    s.addText(item.icon, { x: x + 0.15, y: y + 0.15, w: 0.55, h: 0.55, fontSize: 20, align: "center", valign: "middle" });
    s.addText(item.title, { x: x + 0.8, y: y + 0.18, w: 2.0, h: 0.4, fontSize: 13, bold: true, color: C.navy });
    s.addText(item.body, { x: x + 0.15, y: y + 0.75, w: 2.7, h: 1.0, fontSize: 11, color: "#3D4F6A", valign: "top" });
  });
}

// ── Slide 9: Deployment ───────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s);

  s.addText("Deployment & Stack", { x: 0.5, y: 0.2, w: 9, h: 0.65, fontSize: 28, bold: true, color: C.white, fontFace: "Calibri" });

  // Left — stack list
  s.addShape(pres.ShapeType.roundRect, { x: 0.3, y: 1.0, w: 4.4, h: 4.4, fill: { color: C.navy }, line: { color: C.accent, pt: 1 }, rectRadius: 0.1 });
  s.addText("Tech Stack", { x: 0.45, y: 1.1, w: 4.0, h: 0.4, fontSize: 16, bold: true, color: C.iceBlue });

  const stack = [
    ["Backend", "FastAPI + Uvicorn"],
    ["Embedding", "sentence-transformers (local)"],
    ["Vector Store", "FAISS (in-memory + disk)"],
    ["LLM", "OpenAI gpt-4o-mini"],
    ["Data", "Stack Overflow (Kaggle)"],
    ["Tests", "pytest — 28 tests"],
    ["Container", "Docker + docker-compose"],
  ];
  stack.forEach(([k, v], i) => {
    s.addText(k + ":", { x: 0.5, y: 1.65 + i * 0.48, w: 1.6, h: 0.38, fontSize: 11, bold: true, color: C.gray });
    s.addText(v, { x: 2.1, y: 1.65 + i * 0.48, w: 2.4, h: 0.38, fontSize: 11, color: C.white });
  });

  // Right — deploy options
  s.addShape(pres.ShapeType.roundRect, { x: 5.0, y: 1.0, w: 4.7, h: 4.4, fill: { color: C.navy }, line: { color: C.accent, pt: 1 }, rectRadius: 0.1 });
  s.addText("Deployment Options", { x: 5.15, y: 1.1, w: 4.3, h: 0.4, fontSize: 16, bold: true, color: C.iceBlue });

  const deploys = [
    { p: "Render / Railway", s: "Push-to-deploy from GitHub\nFree tier + easy env vars" },
    { p: "HF Spaces (Docker)", s: "GPU support optional\nModel cached between starts" },
    { p: "Local (Docker)", s: "docker compose up --build\nMounts data/ and index/ dirs" },
  ];
  deploys.forEach((d, i) => {
    s.addShape(pres.ShapeType.roundRect, { x: 5.15, y: 1.65 + i * 1.2, w: 4.4, h: 1.0, fill: { color: C.blue }, line: { color: C.iceBlue, pt: 0 }, rectRadius: 0.08 });
    s.addText(d.p, { x: 5.3, y: 1.72 + i * 1.2, w: 4.1, h: 0.3, fontSize: 12, bold: true, color: C.white });
    s.addText(d.s, { x: 5.3, y: 2.02 + i * 1.2, w: 4.1, h: 0.5, fontSize: 10, color: C.iceBlue });
  });

  s.addText("See README.md for full setup instructions", {
    x: 5.15, y: 4.7, w: 4.4, h: 0.45, fontSize: 11, color: C.gray, align: "center",
  });
}

// ── Slide 10: Summary ─────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  darkBg(s);

  // Top bar
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: 10, h: 0.08, fill: { color: C.accent }, line: { color: C.accent } });

  s.addText("Summary & Deliverables", {
    x: 0.5, y: 0.25, w: 9, h: 0.7, fontSize: 32, bold: true, color: C.white, fontFace: "Calibri",
  });

  const deliverables = [
    { icon: "✅", text: "RAG Pipeline — FAISS retrieval + OpenAI generation, grounded in 50k SO Q&As" },
    { icon: "✅", text: "FastAPI — POST /ask + GET /health with full Pydantic validation" },
    { icon: "✅", text: "28 pytest tests — structure, 10 diverse queries, edge cases, validation" },
    { icon: "✅", text: "Docker + docker-compose for one-command deployment" },
    { icon: "✅", text: "README with setup, .env.example, and Kaggle data download script" },
    { icon: "📊", text: "test_results.md — 10 TC results with observations & failure analysis" },
    { icon: "🚀", text: "Scales via async I/O, Redis cache, Pinecone, K8s HPA" },
  ];

  deliverables.forEach((d, i) => {
    s.addShape(pres.ShapeType.roundRect, { x: 0.4, y: 1.15 + i * 0.58, w: 9.2, h: 0.5, fill: { color: i < 5 ? C.blue : C.navy }, line: { color: C.iceBlue, pt: 0 }, rectRadius: 0.06 });
    s.addText(d.icon + "  " + d.text, { x: 0.55, y: 1.18 + i * 0.58, w: 8.8, h: 0.44, fontSize: 12.5, color: C.white, valign: "middle" });
  });

  s.addText("github.com/<your-username>/python-qa-assistant", {
    x: 0, y: 5.15, w: 10, h: 0.35, fontSize: 11, color: C.gray, align: "center",
  });
}

// ── Write file ───────────────────────────────────────────────────────────────
pres.writeFile({ fileName: "/home/claude/python-qa-assistant/slides/Python_QA_Assistant.pptx" })
  .then(() => console.log("✓ Deck written"))
  .catch(e => { console.error(e); process.exit(1); });
