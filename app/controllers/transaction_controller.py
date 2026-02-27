from datetime import date
from decimal import Decimal, InvalidOperation

from flask import flash, redirect, render_template, request, session, url_for

from app.messages import INVALID_TRANSACTION, MISSING_FIELDS
from app.models import add_transaction
from app.services import session_service


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
    transaction_type_raw = request.form.get("transaction_type", "").strip()
    transaction_genre = request.form.get("genre", "").strip().lower()

    if not all([name, transaction_date_raw, amount_raw, transaction_type_raw, transaction_genre]):
        flash(MISSING_FIELDS, "error")
        return redirect(url_for("main.transactions_page"))

    try:
        transaction_date = date.fromisoformat(transaction_date_raw)
        amount = Decimal(amount_raw)
    except (ValueError, InvalidOperation):
        flash(INVALID_TRANSACTION, "error")
        return redirect(url_for("main.transactions_page"))

    transaction_type = {"debit": "Debit", "credit": "Credit"}.get(transaction_type_raw.lower())

    if amount <= 0 or transaction_type is None:
        flash(INVALID_TRANSACTION, "error")
        return redirect(url_for("main.transactions_page"))

    user_id = session.get("user_id")
    created_transaction_id = add_transaction(
        user_id,
        name,
        transaction_date,
        amount,
        transaction_type,
        transaction_genre,
    )
    if created_transaction_id is None:
        flash(INVALID_TRANSACTION, "error")
        return redirect(url_for("main.transactions_page"))

    return redirect(url_for("main.transactions_page"))
