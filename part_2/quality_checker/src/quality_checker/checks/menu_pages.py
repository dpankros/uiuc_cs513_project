import sqlite3
from tabulate import tabulate
from quality_checker.db import run_query
from quality_checker.models.menu_page import menu_page_factory


def check_menu_pages(conn: sqlite3.Connection) -> str:
    query = """
    select * from MenuPage MP
    left outer join main.Menu M on M.id = MP.menu_id
    where M.id is NULL;
    """
    results = run_query(conn, query=query, row_factory=menu_page_factory)
    headers = ["relation with broken foreign keys", "number broken"]
    data = [("Menu", len(results))]
    return tabulate(tabular_data=data, headers=headers, tablefmt="grid")
