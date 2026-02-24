import psycopg2

from app.models.db import execute

def add_user(name, email, password):
    try:
        cursor = execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id",
            (name, email, password),
            commit=True,
        )
        row = cursor.fetchone()
        return row[0] if row else None
    except psycopg2.IntegrityError:
        return None
    except psycopg2.Error:
        return None


def get_user_by_email(email):
    try:
        row = execute(
            "SELECT id, name, email, password FROM users WHERE email = %s",
            (email,),
        ).fetchone()
        return row
    except psycopg2.Error:
        return None


def set_session_token(user_id, token):
    try:
        cursor = execute(
            "UPDATE users SET session_token = %s WHERE id = %s",
            (token, user_id),
            commit=True,
        )
        return cursor.rowcount
    except psycopg2.Error:
        return 0


def get_session_token(user_id):
    try:
        row = execute(
            "SELECT session_token FROM users WHERE id = %s",
            (user_id,),
        ).fetchone()
        return row[0] if row else None
    except psycopg2.Error:
        return None


def clear_session_token(user_id=None, token=None):
    if user_id:
        try:
            cursor = execute(
                "UPDATE users SET session_token = NULL WHERE id = %s",
                (user_id,),
                commit=True,
            )
            return cursor.rowcount
        except psycopg2.Error:
            return 0

    if token:
        try:
            cursor = execute(
                "UPDATE users SET session_token = NULL WHERE session_token = %s",
                (token,),
                commit=True,
            )
            return cursor.rowcount
        except psycopg2.Error:
            return 0

    return 0
