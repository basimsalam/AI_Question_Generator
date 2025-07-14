# 📄 AI Question Paper Generator – README

## 📌 Project Overview

This is an AI-powered FastAPI application that dynamically generates question papers from a subject-wise knowledge base using LLaMA 3 via the Groq API. Teachers can generate MCQs, short answers, and long answer questions, download them as PDF or Word files, and avoid duplication using Redis caching.

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.9+
- Redis server running locally (or Redis Cloud URL)
- Groq API Key

### 📦 Installation

```bash
git clone https://github.com/your-username/ai-question-generator.git
cd ai-question-generator
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### ⚙️ Environment Setup

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key
REDIS_URL=redis://localhost:6379
```

### ▶️ Run the Application

```bash
uvicorn app.main:app --reload
```

Then navigate to: [http://localhost:8000/docs](http://localhost:8000/docs) to access Swagger UI.

---

## 📁 Directory Structure

```
app/
├── main.py                # FastAPI app entrypoint
├── routes.py              # API endpoints
├── models/schema.py       # Pydantic models
├── services/
│   ├── generator.py       # LLM interaction logic
│   └── knowledge_base.py  # Curriculum JSON loader
├── utils/
│   ├── caching.py         # Redis-based deduplication/cache
│   ├── document_generator.py # PDF/Word export
│   └── response_formatter.py # Unified response format
├── data/sample_kb.json    # Knowledge base for subjects
├── generated_papers/      # Output PDFs and Word docs
```

---

## ✅ Assumptions Made

- Subject knowledge is encoded in structured JSON files.
- Teachers want MCQs, short, and long answer types.
- Grade and topic coverage is fixed to the input knowledge base.
- Redis is available for deduplication and caching.
- Groq LLaMA-3 is available for inference.

---

## 💡 Design Decisions & Trade-offs

| Feature             | Decision                                                           |
| ------------------- | ------------------------------------------------------------------ |
| Model choice        | LLaMA 3 via Groq API for open, fast inference                      |
| Deduplication       | Redis set-based storage per user per session                       |
| Format flexibility  | Supports MCQ, Short Answer, and Long Answer via structured prompts |
| Document generation | `fpdf` and `python-docx` used instead of heavy LaTeX pipelines     |
| Caching strategy    | Question templates cached by topic, difficulty, type               |

---

## 🧠 AI Integration

- LLaMA 3 is used via `https://api.groq.com/openai/v1/chat/completions`.
- Prompts are built dynamically using the selected topic, difficulty, and type.
- If a knowledge base entry exists, learning objectives and facts are injected.

### 🧾 Prompt Example

```
Generate a clean, exam-ready MCQ question only.
Subject: Biology
Grade: 10
Topic: Photosynthesis
Difficulty: Easy
Objectives: [Define process of photosynthesis...]
Facts: [CO2 + H2O + sunlight = glucose + O2...]
```

---

## 📊 Performance Benchmarking

### Setup:

- Intel i7 CPU, 16 GB RAM, local Redis
- Groq API (LLaMA3-70B)
- Test input: 3 topics, 5 questions

### Results:

| Component            | Time (avg)    |
| -------------------- | ------------- |
| Question generation  | 1.5s/question |
| Caching hit time     | < 20ms        |
| PDF/Word generation  | < 500ms       |
| Total roundtrip time | \~8 seconds   |

### Observations:

- Groq LLaMA3 is extremely fast (\~1.5s for complex long answers).
- Redis cache hits significantly reduce regeneration time.

---

## 🙋 Contact

For questions or support, contact: [basimnnas\@gmail.com]

