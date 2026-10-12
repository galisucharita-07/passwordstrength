
import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "password_history.db"


def get_connection():
    """Create a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the analysis history table if it does not exist."""

    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                score INTEGER NOT NULL,
                strength TEXT NOT NULL,
                password_length INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT
                    (strftime('%Y-%m-%d %H:%M:%S', 'now'))
            )
        """)


def save_analysis(result):
    """Save analysis metadata, never the password itself."""

    with get_connection() as connection:
        cursor = connection.execute("""
            INSERT INTO analysis_history (
                score,
                strength,
                password_length
            )
            VALUES (?, ?, ?)
        """, (
            int(result["score"]),
            str(result["strength"]),
            int(result["length"])
        ))

        return cursor.lastrowid


def get_analysis_history(limit=50):
    """Return the most recent analysis records."""

    limit = max(1, min(int(limit), 100))

    with get_connection() as connection:
        rows = connection.execute("""
            SELECT id, score, strength, password_length, created_at
            FROM analysis_history
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

        return [dict(row) for row in rows]


def clear_analysis_history():
    """Delete all saved analysis records."""

    with get_connection() as connection:
        connection.execute("DELETE FROM analysis_history")
