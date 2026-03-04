import psycopg2

from app.models.db import execute


def add_statement(user_id, bank_file_format_id, name):
    try:
        cursor = execute(
            """
            INSERT INTO statements (
                user_id,
                bank_file_format_id,
                name
            )
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (user_id, bank_file_format_id, name),
            commit=True,
        )
        row = cursor.fetchone()
        return row[0] if row else None
    except psycopg2.Error:
        return None
