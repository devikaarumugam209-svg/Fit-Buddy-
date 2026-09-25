import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent.parent / "fitbuddy.db"


def init_db() -> None:
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS fitness_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                plan TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                height_cm REAL NOT NULL,
                weight_kg REAL NOT NULL,
                goal TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER,
                rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def create_profile(
    name: str,
    age: int,
    height_cm: float,
    weight_kg: float,
    goal: str,
) -> dict:
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute(
            """
            INSERT INTO profiles (name, age, height_cm, weight_kg, goal)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, age, height_cm, weight_kg, goal),
        )
        profile_id = cursor.lastrowid

    return get_profile(profile_id)


def get_profile(profile_id: int) -> dict | None:
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT * FROM profiles WHERE id = ?",
            (profile_id,),
        ).fetchone()

    return dict(row) if row else None


def save_fitness_plan(name: str, plan: str) -> int:
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute(
            "INSERT INTO fitness_plans (name, plan) VALUES (?, ?)",
            (name, plan),
        )
        return cursor.lastrowid


def get_latest_fitness_plan(name: str) -> str | None:
    with sqlite3.connect(DATABASE_PATH) as connection:
        row = connection.execute(
            "SELECT plan FROM fitness_plans WHERE name = ? "
            "ORDER BY created_at DESC, id DESC LIMIT 1",
            (name,),
        ).fetchone()

    return row[0] if row else None


def save_feedback(profile_id: int | None, rating: int, message: str) -> int:
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute(
            "INSERT INTO feedback (profile_id, rating, message) VALUES (?, ?, ?)",
            (profile_id, rating, message),
        )
        return cursor.lastrowid


def get_profiles_with_feedback() -> list[dict]:
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.row_factory = sqlite3.Row
        profiles = connection.execute(
            "SELECT id, name, age, height_cm, weight_kg, goal, created_at "
            "FROM profiles ORDER BY created_at DESC, id DESC"
        ).fetchall()
        feedback_rows = connection.execute(
            "SELECT id, profile_id, rating, message, created_at "
            "FROM feedback ORDER BY created_at DESC, id DESC"
        ).fetchall()

    feedback_by_profile: dict[int, list[dict]] = {}
    for row in feedback_rows:
        feedback_by_profile.setdefault(row["profile_id"], []).append(dict(row))

    return [
        {
            **dict(profile),
            "feedback": feedback_by_profile.get(profile["id"], []),
        }
        for profile in profiles
    ]