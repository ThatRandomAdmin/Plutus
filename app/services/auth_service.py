import uuid

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import (
    add_user,
    clear_session_token,
    create_invite_link as create_invite_link_model,
    get_invite_link,
    get_user_by_email,
    set_session_token,
    use_invite_link,
)


def authenticate(email, password):
    row = get_user_by_email(email)
    if not row:
        return None

    user_id, name, _, password_hash, is_admin, group_code = row
    return (user_id, name, is_admin, group_code) if check_password_hash(password_hash, password) else None


def create_user(name, email, password):
    password_hash = generate_password_hash(password)
    group_code = uuid.uuid4().hex[:8].upper()
    new_user_id = add_user(name, email, password_hash, True, group_code)
    if new_user_id is None:
        return None
    return new_user_id, group_code


def create_invited_user(name, email, password, group_code):
    password_hash = generate_password_hash(password)
    return add_user(name, email, password_hash, False, group_code)


def create_invite_link(admin_user_id, group_code):
    invite_token = uuid.uuid4().hex
    invite_id = create_invite_link_model(admin_user_id, group_code, invite_token)
    if invite_id is None:
        return None
    return invite_token


def read_invite(invite_token):
    row = get_invite_link(invite_token)
    if not row:
        return None
    return {
        "id": row[0],
        "admin_user_id": row[1],
        "group_code": row[2],
        "token": row[3],
        "used": row[4],
    }


def mark_invite_used(invite_token, used_by_user_id):
    return use_invite_link(invite_token, used_by_user_id)


def start_session(user_id, name, is_admin, group_code):
    token = uuid.uuid4().hex
    session["user_id"] = user_id
    session["user_name"] = name
    session["is_admin"] = bool(is_admin)
    session["group_code"] = group_code
    session["session_token"] = token
    session.permanent = True
    set_session_token(user_id, token)


def logout():
    user_id = session.get("user_id")
    token = session.get("session_token")
    clear_session_token(user_id=user_id, token=token)
    session.clear()
