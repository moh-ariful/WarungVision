# storage_kasbon.py
from datetime import datetime
from typing import List, Dict, Any
from storage import get_connection

def init_db_kasbon() -> None:
    """Inisialisasi tabel log hutang (Kasbon)"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS debt_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            customer_name TEXT,
            items_list TEXT,
            total_amount REAL,
            due_date_note TEXT,
            raw_text TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def log_debt(name: str, items: str, amount: float, due_date: str, raw: str) -> None:
    """Simpan data hutang ke database"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO debt_logs (created_at, customer_name, items_list, total_amount, due_date_note, raw_text)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (datetime.utcnow().isoformat(), name, items, amount, due_date, raw),
    )
    conn.commit()
    conn.close()

def get_recent_debts(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Ambil daftar riwayat hutang terakhir.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, customer_name, items_list, total_amount, due_date_note, created_at
        FROM debt_logs
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        results.append({
            "id": row["id"],
            "customer_name": row["customer_name"],
            "items": row["items_list"],
            "amount": row["total_amount"],
            "due_date": row["due_date_note"],
            "created_at": row["created_at"]
        })
    return results