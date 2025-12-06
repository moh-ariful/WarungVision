# storage.py
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional

DB_PATH = Path("warungvision.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    cur = conn.cursor()

    # Log verifikasi transfer
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS transfer_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            notes TEXT,
            result_text TEXT
        )
        """
    )

    # Log analisis inventory
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS inventory_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            notes TEXT,
            result_text TEXT
        )
        """
    )

    conn.commit()
    conn.close()


def log_transfer(notes: str, result_text: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO transfer_logs (created_at, notes, result_text)
        VALUES (?, ?, ?)
        """,
        (datetime.utcnow().isoformat(), notes, result_text),
    )
    conn.commit()
    conn.close()


def log_inventory(notes: str, result_text: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO inventory_logs (created_at, notes, result_text)
        VALUES (?, ?, ?)
        """,
        (datetime.utcnow().isoformat(), notes, result_text),
    )
    conn.commit()
    conn.close()
