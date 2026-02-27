import psycopg2

from app.models.db import execute


def add_bank_transaction(
    user_id,
    bank_file_format_id,
    name,
    transaction_date,
    amount,
    transaction_type,
):
    try:
        insert_cursor = execute(
            """
            INSERT INTO "bankTransactions" (
                user_id,
                bank_file_format_id,
                name,
                transaction_date,
                amount,
                transaction_type
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                user_id,
                bank_file_format_id,
                name,
                transaction_date,
                amount,
                transaction_type,
            ),
            commit=True,
        )
        inserted_row = insert_cursor.fetchone()
        return inserted_row[0] if inserted_row else None
    except psycopg2.Error:
        return None
