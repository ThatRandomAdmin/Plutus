from psycopg2 import Error, sql
from flask import flash, redirect, render_template, request, session, url_for

from app.models.db import execute
from app.services import session_service

PAGE_SIZE = 20
LOCKED_COLUMNS = {
    "admin",
    "created_at",
    "group_code",
    "id",
    "invite_token",
    "password",
    "session_token",
    "used",
    "used_at",
}


def record_viewer_page():
    if not session_service.is_logged_in():
        session.clear()
        return redirect(url_for("main.home"))
    group_code = session.get("group_code", "")
    is_admin = bool(session.get("is_admin"))
    source = request.form if request.method == "POST" else request.args

    try:
        table_rows = execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            ORDER BY table_name
            """
        ).fetchall()
        tables = [row[0] for row in table_rows]
    except Error:
        tables = []

    selected_table = source.get("table", "").strip()
    if request.method == "POST" and selected_table and selected_table not in tables:
        flash("This table could not be loaded.", "error")
        return redirect(url_for("main.record_viewer_page"))
    if tables and selected_table not in tables:
        selected_table = tables[0]

    try:
        page = int(source.get("page", "1"))
    except ValueError:
        page = 1

    columns = []
    editable_columns = []
    rows = []
    total_rows = 0
    total_pages = 1

    if selected_table:
        try:
            column_rows = execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = %s
                ORDER BY ordinal_position
                """,
                (selected_table,),
            ).fetchall()
            columns = [row[0] for row in column_rows]
            editable_columns = [
                column
                for column in columns
                if column not in LOCKED_COLUMNS and not column.endswith("_id")
            ]

            if request.method == "POST":
                action = source.get("action", "").strip()
                try:
                    row_id = int(source.get("row_id", "0"))
                except ValueError:
                    row_id = 0

                if row_id < 1:
                    flash("Row was not found.", "error")
                elif action == "delete":
                    if not is_admin:
                        flash("Only admins can delete rows.", "error")
                    else:
                        delete_query = sql.SQL(
                            "DELETE FROM {} WHERE id = %s AND group_code = %s RETURNING id"
                        ).format(sql.Identifier(selected_table))
                        deleted_row = execute(
                            delete_query,
                            (row_id, group_code),
                            commit=True,
                        ).fetchone()
                        if deleted_row:
                            flash("Row deleted.", "success")
                        else:
                            flash("Row was not found.", "error")
                elif action == "update":
                    if editable_columns:
                        assignments = [
                            sql.SQL("{} = %s").format(sql.Identifier(column))
                            for column in editable_columns
                        ]
                        values = [source.get(column, "").strip() for column in editable_columns]
                        update_query = (
                            sql.SQL("UPDATE {} SET ").format(sql.Identifier(selected_table))
                            + sql.SQL(", ").join(assignments)
                            + sql.SQL(" WHERE id = %s AND group_code = %s RETURNING id")
                        )
                        updated_row = execute(
                            update_query,
                            tuple(values + [row_id, group_code]),
                            commit=True,
                        ).fetchone()
                        if updated_row:
                            flash("Row updated.", "success")
                        else:
                            flash("Row was not found.", "error")
                    else:
                        flash("This table cannot be updated here.", "error")
                else:
                    flash("This action is invalid.", "error")

                return redirect(
                    url_for("main.record_viewer_page", table=selected_table, page=page)
                )

            if columns:
                count_query = sql.SQL(
                    "SELECT COUNT(*) FROM {} WHERE group_code = %s"
                ).format(sql.Identifier(selected_table))
                total_rows = execute(count_query, (group_code,)).fetchone()[0]
                total_pages = max(1, (total_rows + PAGE_SIZE - 1) // PAGE_SIZE)
                page = max(1, min(page, total_pages))
                offset = (page - 1) * PAGE_SIZE

                data_query = sql.SQL(
                    "SELECT * FROM {} WHERE group_code = %s ORDER BY id LIMIT %s OFFSET %s"
                ).format(sql.Identifier(selected_table))
                data_rows = execute(
                    data_query,
                    (group_code, PAGE_SIZE, offset),
                ).fetchall() or []
                rows = [dict(zip(columns, row)) for row in data_rows]
        except Error:
            columns = []
            editable_columns = []
            rows = []
            total_rows = 0
            total_pages = 1
            page = 1
            if request.method == "POST":
                flash("Could not save that row.", "error")
                return redirect(
                    url_for("main.record_viewer_page", table=selected_table, page=page)
                )

    return render_template(
        "postlogin/record_viewer.html",
        tables=tables,
        selected_table=selected_table,
        columns=columns,
        editable_columns=editable_columns,
        rows=rows,
        total_rows=total_rows,
        page=page,
        total_pages=total_pages,
        is_admin=is_admin,
    )
