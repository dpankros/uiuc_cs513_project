import sqlite3
import click
import io

from quality_checker.checks.menu import check_menus
from quality_checker.checks.menu_pages import check_menu_pages
from quality_checker.checks import Check
from quality_checker.checks.table_counts import check_table_counts
from quality_checker.checks.menu_items import check_menu_items


def check_all(conn: sqlite3.Connection) -> str:
    with io.StringIO() as str_io:
        checks_to_run = ["table_counts", "menu_items", "menu_pages"]
        for check_name in checks_to_run:
            title, checker = CHECK_TYPE_TO_IMPL[check_name]
            res = checker(conn)
            str_io.write(f"({check_name}) {title}\n{res}\n\n")
        return str_io.getvalue()


CHECK_TYPE_TO_IMPL: dict[str, Check] = {
    "all": ("Run all checks", check_all),
    "table_counts": ("Listing the number of rows in each table", check_table_counts),
    "menu_items": (
        "Listing the numbers of broken foreign key relations in the MenuItems table",
        check_menu_items,
    ),
    "menu_pages": (
        "Listing the numbers of broken foreign key relations in the MenuPages table",
        check_menu_pages,
    ),
    "menu": (
        "Listing integrity constraint violations in the Menu table",
        check_menus,
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
        title, checker = CHECK_TYPE_TO_IMPL[check_type]
        result = checker(conn)
        print(f"{title}\n")
        print(result)
    return 0
