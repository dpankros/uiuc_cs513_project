import sqlite3
import click

from quality_checker.checks import Check
from quality_checker.checks.table_counts import check_table_counts
from quality_checker.checks.menu_items import check_menu_items


CHECK_TYPE_TO_IMPL: dict[str, Check] = {
    "table_counts": ("Listing the number of rows in each table", check_table_counts),
    "menu_items": (
        "Listing the number of broken foreign key relations in the MenuItems table",
        check_menu_items,
    ),
}

DB_PATH = "../../data.sqlite"


@click.command()
@click.option("--check-type", default="table_counts", help="The type of check to run")
def main(check_type: str) -> int:
    if check_type not in CHECK_TYPE_TO_IMPL:
        print(f"unknown check type {check_type}")
    else:
        conn = sqlite3.Connection(DB_PATH)
        print(f"Running {check_type} check...")
        title, checker = CHECK_TYPE_TO_IMPL[check_type]
        result = checker(conn)
        print("\n")
        print(title)
        print(result)
    return 0
