import sqlite3
import os

# Caminho fixo do banco (relativo ao diretório backend/src) para não criar vários database.db
DB_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(DB_DIR, "database.db")


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn