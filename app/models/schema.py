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
    """,
    """
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        name TEXT NOT NULL,
        transaction_date DATE NOT NULL,
        amount NUMERIC(12,2) NOT NULL,
        transaction_type TEXT NOT NULL,
        transaction_genre TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS bank_file_formats (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
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
    CREATE TABLE IF NOT EXISTS "bankTransactions" (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        bank_file_format_id INTEGER NOT NULL REFERENCES bank_file_formats(id) ON DELETE RESTRICT,
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
