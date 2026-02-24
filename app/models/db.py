import os
from urllib.parse import urlparse

import psycopg2

_conn = None


def _default_sslmode(db_url):
    host = (urlparse(db_url).hostname or "").lower()
    if host in {"localhost", "127.0.0.1", "::1"}:
        return "disable"
    return "require"


def get_conn():
    global _conn
    if _conn is None or _conn.closed:
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL is not set.")
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        if not db_url.startswith("postgresql://"):
            raise ValueError("DATABASE_URL must be a PostgreSQL URL.")

        connect_kwargs = {"connect_timeout": 5}
        if "sslmode=" not in db_url:
            connect_kwargs["sslmode"] = _default_sslmode(db_url)

        _conn = psycopg2.connect(db_url, **connect_kwargs)
    return _conn


def execute(sql, params=(), *, commit=False):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params)
        if commit:
            conn.commit()
        return cursor
    except psycopg2.Error:
        conn.rollback()
        raise
