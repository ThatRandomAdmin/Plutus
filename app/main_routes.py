from flask import Blueprint, render_template

from app.controllers import (
    app_page_controller,
    auth_controller,
    bank_import_controller,
    home_controller,
    reconciliation_controller,
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


@bp.route("/settings")
def settings_page():
    return auth_controller.settings_page()


@bp.route("/settings/invite", methods=["POST"])
def generate_invite_link():
    return auth_controller.generate_invite_link()


@bp.route("/invite/<token>")
def invite_signup_page(token):
    return auth_controller.invite_signup_page(token)


@bp.route("/invite/<token>/signup", methods=["POST"])
def invite_signup(token):
    return auth_controller.invite_signup(token)


@bp.route("/app")
def app_page():
    return app_page_controller.app_page()


@bp.route("/transactions")
def transactions_page():
    return transaction_controller.transactions_page()


@bp.route("/transactions", methods=["POST"])
def create_transaction():
    return transaction_controller.create_transaction()


@bp.route("/bank-import")
def bank_import_page():
    return bank_import_controller.bank_import_page()


@bp.route("/bank-import/formats", methods=["POST"])
def create_bank_file_format():
    return bank_import_controller.create_bank_file_format()


@bp.route("/bank-import/upload", methods=["POST"])
def upload_bank_file():
    return bank_import_controller.upload_bank_file()


@bp.route("/reconcile", methods=["GET", "POST"])
def reconcile_page():
    return reconciliation_controller.reconcile_page()


@bp.route("/record-viewer", methods=["GET", "POST"])
def record_viewer_page():
    return record_viewer_controller.record_viewer_page()


@bp.route("/mobile")
def mobile_blocked():
    return render_template("errors/mobile.html"), 403
