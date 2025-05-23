import sqlite3
import time

def init_db():
    """
    Create logs table if not exists.
    """
    with sqlite3.connect("logs.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY,
                session_id TEXT,
                document_id TEXT,
                question TEXT,
                answer TEXT,
                context TEXT,
                timestamp REAL,
                latency REAL
            )
        """)

def log_query(session_id, document_id, question, answer, context, latency):
    """
    Log each query and response to the database
    """
    with sqlite3.connect("logs.db") as conn:
        conn.execute("""
            INSERT INTO logs (session_id, document_id, question, answer, context, timestamp, latency)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (session_id, document_id, question, answer, context, time.time(), latency))

def get_history(session_id):
    """
    Retrieve all past queries for a given session.
    """
    with sqlite3.connect("logs.db") as conn:
        cur = conn.execute("SELECT question, answer, context, timestamp FROM logs WHERE session_id = ?", (session_id,))
        return [dict(zip([c[0] for c in cur.description], row)) for row in cur.fetchall()]