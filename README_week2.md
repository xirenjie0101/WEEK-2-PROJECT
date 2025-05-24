# 📄 Week 2 — RAG-Based Document QA System Frontend

Week 2 project builds upon the core components of Week 1 project and adds:

- A FastAPI backend for querying and uploading documents
- A simple Streamlit frontend for interactive use
- Logging, session tracking, and performance metrics
- Containerization for easy deployment

---

## Features

### Backend API (FastAPI)
- `POST /upload`: Upload the TXT document 
- `POST /query`: Ask a question and receive an answer
- `GET /history`: Retrieve history questions 
- `GET /metrics`: See metrics (query count and average latency)

###  Frontend UI (Streamlit)
- Upload a document
- Ask questions via chat box
- View results with context

###  Logging & Observability
- Logs queries, answers, and latency to SQLite
- Structured logs via Python `logging`
- Easily extended for Prometheus/Grafana

---

##  Project Structure

```
├── app/                 # Week 1 logic (imported, not modified)
├── main.py              # FastAPI server
├── streamlit_app.py     # Streamlit frontend UI
├── db.py                # SQLite-based session/query logger
├── utils.py             # Glue code to wrap app modules
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── storage/             # Uploaded files and FAISS indexes
```

---

##  How to Run

###  1. Install dependencies

```bash
pip install -r requirements.txt
```

### ▶ 2. Run FastAPI app

```bash
uvicorn main:app --reload
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI

---

###  3. Optional: Run Streamlit UI

```bash
streamlit run streamlit_app.py
```

---

###  4. Run with Docker (recommended)

```bash
docker-compose up
```

---

##  Input Format

- Documents: TXT files (extension: `.txt`)
- Questions: Natural language questions via form or API

---

##  Output Format

```json
{
  "answer": "Generated answer here.",
  "context": "Relevant context from document.",
  "latency": 1.42
}
```

---

##  Monitoring

- Endpoint: `GET /metrics`
- Returns total query count + average latency

---

##  Dependencies

- FastAPI
- Uvicorn
- SentenceTransformers
- FAISS
- SQLite3
- Streamlit
- Docker (optional)

---

