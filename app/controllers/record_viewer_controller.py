from psycopg2 import Error, sql
from flask import redirect, render_template, request, session, url_for

from app.models.db import execute
from app.services import session_service

PAGE_SIZE = 20


def record_viewer_page():
    if not session_service.is_logged_in():
        session.clear()
        return redirect(url_for("main.home"))
    group_code = session.get("group_code", "")

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

    selected_table = request.args.get("table", "").strip()
    if tables and selected_table not in tables:
        selected_table = tables[0]

    try:
        page = int(request.args.get("page", "1"))
    except ValueError:
        page = 1

    columns = []
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

            if columns:
                count_query = sql.SQL(
                    "SELECT COUNT(*) FROM {} WHERE group_code = %s"
                ).format(sql.Identifier(selected_table))
                total_rows = execute(count_query, (group_code,)).fetchone()[0]
                total_pages = max(1, (total_rows + PAGE_SIZE - 1) // PAGE_SIZE)
                page = max(1, min(page, total_pages))
                offset = (page - 1) * PAGE_SIZE

                data_query = sql.SQL(
                    "SELECT * FROM {} WHERE group_code = %s LIMIT %s OFFSET %s"
                ).format(sql.Identifier(selected_table))
                rows = execute(data_query, (group_code, PAGE_SIZE, offset)).fetchall() or []
        except Error:
            columns = []
            rows = []
            total_rows = 0
            total_pages = 1
            page = 1

    return render_template(
        "postlogin/record_viewer.html",
        tables=tables,
        selected_table=selected_table,
        columns=columns,
        rows=rows,
        total_rows=total_rows,
        page=page,
        total_pages=total_pages,
    )
