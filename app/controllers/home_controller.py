from flask import redirect, render_template, url_for

from app.services import session_service


def home():
    if session_service.is_logged_in():
        return redirect(url_for("main.app_page"))
    return render_template("prelogin/home.html")
