from dataclasses import dataclass
import json
import sqlite3
from typing import Literal
import click
import io
from functools import cache

from checker.checks.menu_item_domain import check_menu_item_xpos_ypos_domain
from checker.checks.menu import check_menus
from checker.checks.dish import check_dish
from checker.checks.menu_pages import check_menu_pages
from checker.checks import Check, CheckResult, tabulate_check_formatter
from checker.checks.table_counts import check_table_counts
from checker.checks.menu_items import check_menu_items


CHECK_TYPE_TO_IMPL: dict[str, Check] = {
    "table_counts": ("Listing the number of rows in each table", check_table_counts),
    "menu_items": (
        "Listing the numbers of broken foreign key relations in the MenuItems table",
        check_menu_items,
    ),
    "menu_items_position_domain": (
        "Listing the domain of the xpos and ypos columns in the MenuItems table",
        check_menu_item_xpos_ypos_domain,
    ),
    "menu_pages": (
        "Listing the numbers of broken foreign key relations in the MenuPages table",
        check_menu_pages,
    ),
    "menu": (
        "Listing integrity constraint violations in the Menu table",
        check_menus,
    ),
    "dish": (
        "Listing quality metrics for the Dish table",
        check_dish,
    ),
}


DB_PATH = "../../data.sqlite"


@cache
def _get_conn():
    return sqlite3.Connection(DB_PATH)


@dataclass
class CheckEntry:
    check_name: str
    description: str
    data: CheckResult


_all_check_types = ["all"] + list(CHECK_TYPE_TO_IMPL.keys())


@click.command()
@click.option(
    "--check-type", default="all", help=f"The type of check to run {_all_check_types}"
)
@click.option(
    "--format",
    default="table",
    help="The format in which to output metrics results [table, json]",
)
def main(check_type: str, format: Literal["table", "json"]) -> int:
    if check_type == "all":
        checks_to_run = CHECK_TYPE_TO_IMPL.keys()
        results: list[CheckEntry] = []
        for check_name in checks_to_run:
            descr, checker = CHECK_TYPE_TO_IMPL[check_name]
            data = checker(_get_conn())
            results.append(
                CheckEntry(check_name=check_name, description=descr, data=data)
            )

        print(_generate_output(entries=results, format=format))
    elif check_type not in CHECK_TYPE_TO_IMPL:
        print(f"unknown check type {check_type}")
    else:
        descr, checker = CHECK_TYPE_TO_IMPL[check_type]
        result = CheckEntry(
            check_name=check_type, description=descr, data=checker(_get_conn())
        )
        print(
            _generate_output(entries=[result], format=format),
        )
    return 0


def _generate_output(
    *,
    entries: list[CheckEntry],
    format: Literal["table", "json"],
) -> str:
    match format:
        case "table":
            with io.StringIO() as str_io:
                for check_entry in entries:
                    table_str = tabulate_check_formatter(check_entry.data)
                    str_io.write(
                        f"{check_entry.check_name}: {check_entry.description}\n{table_str}\n\n"
                    )
                return str_io.getvalue()
        case "json":
            json_dict = {
                entry.check_name: {"description": entry.description, "data": entry.data}
                for entry in entries
            }
            return json.dumps(json_dict)
