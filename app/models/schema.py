import psycopg2

from app.models.db import execute

SCHEMA_SQL = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        session_token TEXT,
        admin BOOLEAN DEFAULT FALSE
    )
    """
]


def init_db():
    try:
        for schema_sql in SCHEMA_SQL:
            execute(schema_sql, commit=True)
        return True
    except psycopg2.Error:
        return False
