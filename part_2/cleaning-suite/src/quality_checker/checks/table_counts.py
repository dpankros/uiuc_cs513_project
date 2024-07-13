import sqlite3
from quality_checker.db import run_query
from quality_checker.checks import CheckResult

def check_table_counts(conn: sqlite3.Connection) -> CheckResult:
    counts = _get_table_counts(conn)
    return [
        (table_name, count)
        for (table_name, count) in counts
    ]

def _get_table_counts(conn: sqlite3.Connection) -> list[tuple[str, int]]:
    query = """
    select 'MenuItem', count(*) from MenuItem MI
    union
    select 'Dish', count(*) from Dish D
    union
    select 'Menu', count(*) from Menu M
    union
    select 'MenuPage', count(*) from MenuPage MP;
    """

    def table_counts_factory(
        cursor: sqlite3.Cursor,
        row: sqlite3.Row,
    ) -> tuple[str, int]:
        return row[0], row[1]

    return run_query(conn, query=query, row_factory=table_counts_factory)
