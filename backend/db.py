import json
import sqlite3
from datetime import datetime
from pathlib import Path


DB_PATH = Path(__file__).parent / "profiles.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS profiles (
                linkedin_url TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                current_company TEXT NOT NULL,
                current_role TEXT NOT NULL,
                past_companies TEXT NOT NULL,
                education TEXT NOT NULL,
                raw_text TEXT,
                saved_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


# Create DB/table on import
initialize_db()


def save_profile(profile: dict) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO profiles (
                linkedin_url,
                name,
                current_company,
                current_role,
                past_companies,
                education,
                raw_text,
                saved_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                profile["linkedin_url"],
                profile["name"],
                profile["current_company"],
                profile["current_role"],
                json.dumps(profile["past_companies"]),
                json.dumps(profile["education"]),
                profile.get("raw_text"),
                datetime.utcnow().isoformat(),
            ),
        )
        conn.commit()


def get_profile(linkedin_url: str) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM profiles
            WHERE linkedin_url = ?
            """,
            (linkedin_url,),
        ).fetchone()

    if row is None:
        return None

    return {
        "linkedin_url": row["linkedin_url"],
        "name": row["name"],
        "current_company": row["current_company"],
        "current_role": row["current_role"],
        "past_companies": json.loads(row["past_companies"]),
        "education": json.loads(row["education"]),
        "raw_text": row["raw_text"],
        "saved_at": row["saved_at"],
    }


def list_profiles() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM profiles
            ORDER BY saved_at DESC
            """
        ).fetchall()

    profiles = []

    for row in rows:
        profiles.append(
            {
                "linkedin_url": row["linkedin_url"],
                "name": row["name"],
                "current_company": row["current_company"],
                "current_role": row["current_role"],
                "past_companies": json.loads(row["past_companies"]),
                "education": json.loads(row["education"]),
                "raw_text": row["raw_text"],
                "saved_at": row["saved_at"],
            }
        )

    return profiles


if __name__ == "__main__":
    test_profile = {
        "linkedin_url": "https://linkedin.com/in/john-doe",
        "name": "John Doe",
        "current_company": "Google",
        "current_role": "Software Engineer",
        "past_companies": ["Amazon"],
        "education": ["Stanford University"],
        "raw_text": "Sample profile text",
    }

    save_profile(test_profile)

    result = get_profile(test_profile["linkedin_url"])

    print("Retrieved profile:")
    print(json.dumps(result, indent=2))