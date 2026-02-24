import uuid

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import (
    add_user,
    clear_session_token,
    get_user_by_email,
    set_session_token,
)


def authenticate(email, password):
    row = get_user_by_email(email)
    if not row:
        return None

    user_id, name, _, password_hash = row
    return (user_id, name) if check_password_hash(password_hash, password) else None


def create_user(name, email, password):
    password_hash = generate_password_hash(password)
    return add_user(name, email, password_hash)


def start_session(user_id, name):
    token = uuid.uuid4().hex
    session["user_id"] = user_id
    session["user_name"] = name
    session["session_token"] = token
    session.permanent = True
    set_session_token(user_id, token)


def logout():
    user_id = session.get("user_id")
    token = session.get("session_token")
    clear_session_token(user_id=user_id, token=token)
    session.clear()
