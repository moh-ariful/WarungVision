# storage_tangkal_tipu.py
import sqlite3
from datetime import datetime
from storage import get_connection

def init_db_scam() -> None:
    """Inisialisasi tabel khusus fitur Tangkal Tipu"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS scam_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            extracted_text TEXT,
            extracted_url TEXT,
            verdict TEXT,
            raw_analysis TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def log_scam_check(text: str, url: str, verdict: str, raw_analysis: str) -> None:
    """Simpan log pengecekan scam"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO scam_logs (created_at, extracted_text, extracted_url, verdict, raw_analysis)
        VALUES (?, ?, ?, ?, ?)
        """,
        (datetime.utcnow().isoformat(), text, url, verdict, raw_analysis),
    )
    conn.commit()
    conn.close()