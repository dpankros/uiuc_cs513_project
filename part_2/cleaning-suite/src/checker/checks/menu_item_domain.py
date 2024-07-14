import sqlite3
from typing import Any
from checker.db import run_query
from checker.checks import CheckResult


def check_menu_item_xpos_ypos_domain(conn: sqlite3.Connection) -> CheckResult:
    def domain_factory(
        row_dict: dict[str | Any, Any],
    ) -> tuple[float, float, float, float]:
        row_data = list(row_dict.values())
        return (
            float(row_data[0]),
            float(row_data[1]),
            float(row_data[2]),
            float(row_data[3]),
        )

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
