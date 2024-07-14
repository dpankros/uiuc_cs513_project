import sqlite3
from checker.db import run_query
from checker.models.menu_page import menu_page_factory
from checker.checks import CheckResult


def check_menu_pages(conn: sqlite3.Connection) -> CheckResult:
    query = """
    select * from MenuPage MP
    left outer join main.Menu M on M.id = MP.menu_id
    where M.id is NULL;
    """
    broken_foreign_keys = run_query(conn, query=query, row_factory=menu_page_factory)
    distinct_uuids = run_query(
        conn,
        query="select distinct uuid from MenuPage order by uuid asc;",
        row_factory=lambda row_dict: list(row_dict.values())[0],
    )
    total_menus = run_query(
        conn,
        query="select MP.id from MenuPage MP",
        row_factory=lambda row_dict: list(row_dict.values())[0],
    )
    return [
        ("Duplicate UUIDs", len(total_menus) - len(distinct_uuids)),
        ("Menu.id <> MenuPage.menu_id FK violations", len(broken_foreign_keys)),
    ]
