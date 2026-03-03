from database.db import get_connection

def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,
        filename TEXT,
        type TEXT,
        status TEXT,
        created_at TEXT,
        validation_reason TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS status_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id TEXT,
        status_anterior TEXT,
        status_novo TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()