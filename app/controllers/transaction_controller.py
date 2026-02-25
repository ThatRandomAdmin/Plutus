from datetime import date
from decimal import Decimal, InvalidOperation

from flask import flash, redirect, render_template, request, session, url_for

from app.messages import INVALID_TRANSACTION, MISSING_FIELDS
from app.models import add_transaction
from app.services import session_service

VALID_TRANSACTION_TYPES = {"debit", "credit"}


def transactions_page():
    if not session_service.is_logged_in():
        session.clear()
        return redirect(url_for("main.home"))

    return render_template("postlogin/transactions.html")


def create_transaction():
    if not session_service.is_logged_in():
        session.clear()
        return redirect(url_for("main.home"))

    name = request.form.get("name", "").strip()
    transaction_date_raw = request.form.get("date", "").strip()
    amount_raw = request.form.get("amount", "").strip()
    transaction_type = request.form.get("transaction_type", "").strip().lower()
    transaction_genre = request.form.get("genre", "").strip().lower()

    if (
        not name
        or not transaction_date_raw
        or not amount_raw
        or not transaction_type
        or not transaction_genre
    ):
        flash(MISSING_FIELDS, "error")
        return redirect(url_for("main.transactions_page"))

    try:
        transaction_date = date.fromisoformat(transaction_date_raw)
        amount = Decimal(amount_raw)
    except (ValueError, InvalidOperation):
        flash(INVALID_TRANSACTION, "error")
        return redirect(url_for("main.transactions_page"))

    if amount <= 0 or transaction_type not in VALID_TRANSACTION_TYPES:
        flash(INVALID_TRANSACTION, "error")
        return redirect(url_for("main.transactions_page"))

    user_id = session.get("user_id")
    new_transaction_id = add_transaction(
        user_id,
        name,
        transaction_date,
        amount,
        transaction_type,
        transaction_genre,
    )
    if new_transaction_id is None:
        flash(INVALID_TRANSACTION, "error")

    return redirect(url_for("main.transactions_page"))
