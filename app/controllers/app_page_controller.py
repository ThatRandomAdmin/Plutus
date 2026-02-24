from flask import redirect, render_template, session, url_for

from app.services import session_service


def app_page():
    if not session_service.is_logged_in():
        session.clear()
        return redirect(url_for("main.home"))
    return render_template("postlogin/app.html")
