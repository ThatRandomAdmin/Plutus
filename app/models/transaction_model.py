import psycopg2

from app.models.db import execute


def add_transaction(
    user_id,
    name,
    transaction_date,
    amount,
    transaction_type,
    transaction_genre,
):
    try:
        cursor = execute(
            """
            INSERT INTO transactions (
                user_id,
                name,
                transaction_date,
                amount,
                transaction_type,
                transaction_genre
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                user_id,
                name,
                transaction_date,
                amount,
                transaction_type,
                transaction_genre,
            ),
            commit=True,
        )
        row = cursor.fetchone()
        return row[0] if row else None
    except psycopg2.Error:
        return None
