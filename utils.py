from app.embed import get_embedding_model
from app.chunk import chunk_text
from app.index import build_faiss_index, load_faiss_index
from app.answer import get_answer

import pickle
import faiss
import os
import sqlite3
import logging


logger = logging.getLogger(__name__)
model = get_embedding_model()

def process_document(file_path, doc_id):
    """
    Read the uploaded document, chunk it, embed it, and store in FAISS index.
    """
    logger.info(f"Processing document at {file_path} with ID {doc_id}")
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    chunks = chunk_text(text)
    embeddings, index = build_faiss_index(chunks, model)
    faiss.write_index(index, f"storage/{doc_id}.index")
    with open(f"storage/{doc_id}_chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)
    logger.info(f"Document {doc_id} indexed successfully.")

def query_qa(question, doc_id):
    """
    Search the FAISS index for the most relevant chunks and generate an answer.
    """
    logger.info(f"Running QA for doc_id={doc_id}, question='{question}'")
    index = load_faiss_index(f"storage/{doc_id}.index")
    with open(f"storage/{doc_id}_chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    answer, context = get_answer(question, chunks, index, model)
    return answer, context

def get_metrics():
    """
    Return total number of queries and average response latency.
    """
    with sqlite3.connect("logs.db") as conn:
        total = conn.execute("SELECT COUNT(*) FROM logs").fetchone()[0]
        avg_latency = conn.execute("SELECT AVG(latency) FROM logs").fetchone()[0] or 0
        return {"total_queries": total, "avg_latency": avg_latency}