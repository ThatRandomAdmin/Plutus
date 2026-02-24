from flask import session

from app.models import get_session_token


def is_logged_in():
    user_id = session.get("user_id")
    token = session.get("session_token")
    if not user_id or not token:
        return False
    stored_token = get_session_token(user_id)
    return stored_token == token
