from flask import flash, redirect, request, url_for

from app.messages import EMAIL_EXISTS, INVALID_LOGIN, MISSING_FIELDS
from app.services import auth_service


def login():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    if not email or not password:
        flash(INVALID_LOGIN, "error")
        return redirect(url_for("main.home"))

    authenticated_user = auth_service.authenticate(email, password)
    if not authenticated_user:
        flash(INVALID_LOGIN, "error")
        return redirect(url_for("main.home"))

    auth_service.start_session(*authenticated_user)
    return redirect(url_for("main.app_page"))


def signup():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    if not name or not email or not password:
        flash(MISSING_FIELDS, "error")
        return redirect(url_for("main.home"))
    new_id = auth_service.create_user(name, email, password)
    if new_id is None:
        flash(EMAIL_EXISTS, "error")
        return redirect(url_for("main.home"))
    auth_service.start_session(new_id, name)
    return redirect(url_for("main.app_page"))


def logout():
    auth_service.logout()
    return redirect(url_for("main.home"))
