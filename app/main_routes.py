from flask import Blueprint, render_template

from app.controllers import (
    app_page_controller,
    auth_controller,
    home_controller,
    record_viewer_controller,
    transaction_controller,
)

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    return home_controller.home()


@bp.route("/login", methods=["POST"])
def login():
    return auth_controller.login()


@bp.route("/signup", methods=["POST"])
def signup():
    return auth_controller.signup()


@bp.route("/logout")
def logout():
    return auth_controller.logout()


@bp.route("/app")
def app_page():
    return app_page_controller.app_page()


@bp.route("/transactions")
def transactions_page():
    return transaction_controller.transactions_page()


@bp.route("/transactions", methods=["POST"])
def create_transaction():
    return transaction_controller.create_transaction()


@bp.route("/record-viewer")
def record_viewer_page():
    return record_viewer_controller.record_viewer_page()


@bp.route("/mobile")
def mobile_blocked():
    return render_template("errors/mobile.html"), 403
