import psycopg2

from app.models.db import execute

BANK_FILE_FORMAT_SELECT_COLUMNS = """
                id,
                format_name,
                delimiter,
                date_format,
                data_start_row,
                date_column,
                name_column,
                amount_column,
                debit_amount_column,
                credit_amount_column,
                transaction_type_column
"""


def add_bank_file_format(
    user_id,
    format_name,
    delimiter,
    date_format,
    data_start_row,
    date_column,
    name_column,
    amount_column,
    debit_amount_column,
    credit_amount_column,
    transaction_type_column,
):
    try:
        cursor = execute(
            """
            INSERT INTO bank_file_formats (
                user_id,
                format_name,
                delimiter,
                date_format,
                data_start_row,
                date_column,
                name_column,
                amount_column,
                debit_amount_column,
                credit_amount_column,
                transaction_type_column
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                user_id,
                format_name,
                delimiter,
                date_format,
                data_start_row,
                date_column,
                name_column,
                amount_column,
                debit_amount_column,
                credit_amount_column,
                transaction_type_column,
            ),
            commit=True,
        )
        row = cursor.fetchone()
        return row[0] if row else None
    except psycopg2.Error:
        return None


def get_bank_file_formats_for_user(user_id):
    try:
        return execute(
            f"""
            SELECT
{BANK_FILE_FORMAT_SELECT_COLUMNS}
            FROM bank_file_formats
            WHERE user_id = %s
            ORDER BY format_name ASC, id ASC
            """,
            (user_id,),
        ).fetchall()
    except psycopg2.Error:
        return []


def get_bank_file_format_by_id(user_id, bank_file_format_id):
    try:
        return execute(
            f"""
            SELECT
{BANK_FILE_FORMAT_SELECT_COLUMNS}
            FROM bank_file_formats
            WHERE user_id = %s AND id = %s
            """,
            (user_id, bank_file_format_id),
        ).fetchone()
    except psycopg2.Error:
        return None


def update_bank_file_format(
    user_id,
    bank_file_format_id,
    format_name,
    delimiter,
    date_format,
    data_start_row,
    date_column,
    name_column,
    amount_column,
    debit_amount_column,
    credit_amount_column,
    transaction_type_column,
):
    try:
        cursor = execute(
            """
            UPDATE bank_file_formats
            SET
                format_name = %s,
                delimiter = %s,
                date_format = %s,
                data_start_row = %s,
                date_column = %s,
                name_column = %s,
                amount_column = %s,
                debit_amount_column = %s,
                credit_amount_column = %s,
                transaction_type_column = %s
            WHERE user_id = %s AND id = %s
            RETURNING id
            """,
            (
                format_name,
                delimiter,
                date_format,
                data_start_row,
                date_column,
                name_column,
                amount_column,
                debit_amount_column,
                credit_amount_column,
                transaction_type_column,
                user_id,
                bank_file_format_id,
            ),
            commit=True,
        )
        row = cursor.fetchone()
        return row[0] if row else None
    except psycopg2.Error:
        return None


def delete_bank_file_format(user_id, bank_file_format_id):
    try:
        cursor = execute(
            """
            DELETE FROM bank_file_formats
            WHERE user_id = %s AND id = %s
            RETURNING id
            """,
            (user_id, bank_file_format_id),
            commit=True,
        )
        row = cursor.fetchone()
        return row[0] if row else None
    except psycopg2.Error:
        return None
