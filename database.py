import sqlite3
from datetime import datetime


DATABASE = "screening_history.db"


def init_db():
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS screening_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT,
            match_score REAL,
            matched_skills TEXT,
            missing_skills TEXT,
            screened_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_screening(candidate_name, match_score, matched_skills, missing_skills):
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO screening_history
        (candidate_name, match_score, matched_skills, missing_skills, screened_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        candidate_name,
        match_score,
        ", ".join(matched_skills),
        ", ".join(missing_skills),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_screening_history():
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, candidate_name, match_score,
               matched_skills, missing_skills, screened_at
        FROM screening_history
        ORDER BY id DESC
    """)

    history = cursor.fetchall()

    conn.close()

    return history 
def clear_screening_history():
    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM screening_history")

    conn.commit()
    conn.close() 