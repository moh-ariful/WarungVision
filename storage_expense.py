# storage_expense.py
from datetime import datetime
from typing import List, Dict, Any
from storage import get_connection

def init_db_expense() -> None:
    """Inisialisasi tabel log pengeluaran"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS expense_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            merchant_name TEXT,
            transaction_date TEXT,
            total_amount REAL,
            items_summary TEXT,
            raw_text TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def log_expense(merchant: str, date: str, total: float, items: str, raw: str) -> None:
    """Simpan data belanja ke database"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO expense_logs (created_at, merchant_name, transaction_date, total_amount, items_summary, raw_text)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (datetime.utcnow().isoformat(), merchant, date, total, items, raw),
    )
    conn.commit()
    conn.close()

def get_recent_expenses(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Ambil daftar riwayat belanja terakhir untuk ditampilkan di UI.
    Mengambil data urut dari yang paling baru (DESC).
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, merchant_name, transaction_date, total_amount, items_summary
        FROM expense_logs
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
            "merchant": row["merchant_name"],
            "date": row["transaction_date"],
            "total": row["total_amount"],
            "items": row["items_summary"]
        })
    return results