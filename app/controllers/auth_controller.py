from flask import flash, redirect, render_template, request, session, url_for

from app.messages import EMAIL_EXISTS, INVALID_LOGIN, MISSING_FIELDS
from app.services import auth_service, session_service


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
    created_user = auth_service.create_user(name, email, password)
    if created_user is None:
        flash(EMAIL_EXISTS, "error")
        return redirect(url_for("main.home"))
    new_id, group_code = created_user
    auth_service.start_session(new_id, name, True, group_code)
    return redirect(url_for("main.app_page"))


def logout():
    auth_service.logout()
    return redirect(url_for("main.home"))


def settings_page():
    if not session_service.is_logged_in():
        session.clear()
        return redirect(url_for("main.home"))
    if not session.get("is_admin"):
        return redirect(url_for("main.app_page"))
    return render_template("postlogin/settings.html", invite_link="")


def generate_invite_link():
    if not session_service.is_logged_in():
        session.clear()
        return redirect(url_for("main.home"))
    if not session.get("is_admin"):
        return redirect(url_for("main.app_page"))

    user_id = session.get("user_id")
    group_code = session.get("group_code", "")
    invite_token = auth_service.create_invite_link(user_id, group_code)
    if invite_token is None:
        flash("Could not create invite link.", "error")
        return redirect(url_for("main.settings_page"))

    invite_link = url_for("main.invite_signup_page", token=invite_token, _external=True)
    return render_template("postlogin/settings.html", invite_link=invite_link)


def invite_signup_page(token):
    invite = auth_service.read_invite(token)
    if not invite or invite["used"]:
        flash("Invite link is invalid or already used.", "error")
        return redirect(url_for("main.home"))
    return render_template("prelogin/invite_signup.html", token=token)


def invite_signup(token):
    invite = auth_service.read_invite(token)
    if not invite or invite["used"]:
        flash("Invite link is invalid or already used.", "error")
        return redirect(url_for("main.home"))

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    if not name or not email or not password:
        flash(MISSING_FIELDS, "error")
        return redirect(url_for("main.invite_signup_page", token=token))

    new_id = auth_service.create_invited_user(name, email, password, invite["group_code"])
    if new_id is None:
        flash(EMAIL_EXISTS, "error")
        return redirect(url_for("main.invite_signup_page", token=token))

    used = auth_service.mark_invite_used(token, new_id)
    if not used:
        flash("Invite link is invalid or already used.", "error")
        return redirect(url_for("main.home"))

    auth_service.start_session(new_id, name, False, invite["group_code"])
    return redirect(url_for("main.app_page"))
