# storage_salesman.py
from datetime import datetime
from storage import get_connection

def init_db_salesman() -> None:
    """Init tabel riwayat promosi Salesman WA"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS salesman_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            target_phone TEXT,
            style_used TEXT,
            generated_message TEXT,
            status TEXT,
            api_response TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def log_promotion(target: str, style: str, msg: str, status: str, resp: str) -> None:
    """Catat log pengiriman promosi"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO salesman_logs 
        (created_at, target_phone, style_used, generated_message, status, api_response)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (datetime.utcnow().isoformat(), target, style, msg, status, resp),
    )
    conn.commit()
    conn.close()