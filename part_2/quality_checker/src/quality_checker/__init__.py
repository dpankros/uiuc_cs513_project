import sqlite3
import click
import io
from functools import cache

from quality_checker.checks.menu import check_menus
from quality_checker.checks.menu_pages import check_menu_pages
from quality_checker.checks import Check
from quality_checker.checks.table_counts import check_table_counts
from quality_checker.checks.menu_items import check_menu_items


CHECK_TYPE_TO_IMPL: dict[str, Check] = {
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
@cache
def _get_conn():
        return sqlite3.Connection(DB_PATH)


@click.command()
@click.option("--check-type", default="all", help="The type of check to run")
def main(check_type: str) -> int:
    if check_type == "all":
        checks_to_run = CHECK_TYPE_TO_IMPL.keys()
        print(f"Running all checks ({list(checks_to_run)})")
        with io.StringIO() as str_io:
            for check_name in checks_to_run:
                title, checker = CHECK_TYPE_TO_IMPL[check_name]
                res = checker(_get_conn())
                str_io.write(f"({check_name}) {title}\n{res}\n\n")
            print(str_io.getvalue())
    elif check_type not in CHECK_TYPE_TO_IMPL:
        print(f"unknown check type {check_type}")
    else:
        title, checker = CHECK_TYPE_TO_IMPL[check_type]
        result = checker(_get_conn())
        print(f"{title}\n")
        print(result)
    return 0
