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
        admin BOOLEAN NOT NULL DEFAULT FALSE,
        group_code TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS "groupInvites" (
        id SERIAL PRIMARY KEY,
        admin_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        group_code TEXT NOT NULL,
        invite_token TEXT NOT NULL UNIQUE,
        used BOOLEAN NOT NULL DEFAULT FALSE,
        used_by_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
        used_at TIMESTAMP,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        group_code TEXT NOT NULL,
        name TEXT NOT NULL,
        transaction_date DATE NOT NULL,
        amount NUMERIC(12,2) NOT NULL,
        transaction_type TEXT NOT NULL,
        transaction_genre TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS "bankFileFormats" (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        group_code TEXT NOT NULL,
        format_name TEXT NOT NULL,
        delimiter TEXT NOT NULL,
        date_format TEXT NOT NULL,
        data_start_row INTEGER NOT NULL,
        date_column INTEGER NOT NULL,
        name_column INTEGER NOT NULL,
        amount_column INTEGER,
        debit_amount_column INTEGER,
        credit_amount_column INTEGER,
        transaction_type_column INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS statements (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        bank_file_format_id INTEGER NOT NULL REFERENCES "bankFileFormats"(id) ON DELETE RESTRICT,
        group_code TEXT NOT NULL,
        name TEXT NOT NULL,
        imported_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS "bankTransactions" (
        id SERIAL PRIMARY KEY,
        statement_id INTEGER NOT NULL REFERENCES statements(id) ON DELETE CASCADE,
        group_code TEXT NOT NULL,
        name TEXT NOT NULL,
        transaction_date DATE NOT NULL,
        amount NUMERIC(12,2) NOT NULL,
        transaction_type TEXT NOT NULL
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
