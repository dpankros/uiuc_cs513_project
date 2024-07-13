import sqlite3
from quality_checker.db import run_query
from quality_checker.checks import CheckResult


def check_menu_item_xpos_ypos_domain(conn: sqlite3.Connection) -> CheckResult:
    def domain_factory(
        cursor: sqlite3.Cursor, row: sqlite3.Row
    ) -> tuple[float, float, float, float]:
        return float(row[0]), float(row[1]), float(row[2]), float(row[3])

    query = "select min(xpos), max(xpos), min(ypos), max(ypos) from MenuItem;"
    results = run_query(
        conn,
        query=query,
        row_factory=domain_factory,
    )

    return [
        ("xpos_min", results[0][0]),
        ("xpos_max", results[0][1]),
        ("ypos_min", results[0][2]),
        ("ypos_max", results[0][3]),
    ]
