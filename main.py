from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import uuid, os, time
from utils import process_document, query_qa, get_metrics
from db import init_db, log_query, get_history
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    os.makedirs("storage", exist_ok=True)
    file_path = f"storage/{file_id}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    logger.info(f"Received file: {file.filename} with ID: {file_id}")
    process_document(file_path, file_id)
    logger.info(f"Processed and indexed document: {file_id}")
    return {"document_id": file_id}

@app.post("/query")
async def query(session_id: str = Form(...), question: str = Form(...), document_id: str = Form(...)):
    start = time.time()
    logger.info(f"Query received: '{question}' for document: {document_id} by session: {session_id}")
    answer, context = query_qa(question, document_id)
    latency = time.time() - start
    log_query(session_id, document_id, question, answer, context, latency)
    logger.info(f"Query answered in {latency:.2f} seconds")
    return {"answer": answer, "context": context, "latency": latency}

@app.get("/history")
def history(session_id: str):
    logger.info(f"History requested for session: {session_id}")
    return get_history(session_id)

@app.get("/metrics")
def metrics():
    logger.info("Metrics requested")
    return get_metrics()