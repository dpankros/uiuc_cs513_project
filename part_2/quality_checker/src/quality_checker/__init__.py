import click
from enum import StrEnum
from tabulate import tabulate

from quality_checker.sqlite import get_table_counts, missing_menuitem_data


class CheckType(StrEnum):
    TableCounts = "table_counts"
    MenuItems = "menu_items"


DB_PATH = "../../data.sqlite"


@click.command()
@click.option(
    '--check-type',
    default=CheckType.TableCounts,
    help='The type of check to run'
)
def main(check_type: str) -> int:
    match check_type:
        case CheckType.TableCounts:
            print(f"running check type: {check_type}")
            counts = get_table_counts(DB_PATH)
            print("counts")
            print(tabulate(
                tabular_data=counts,
                headers=["table", "count"],
                tablefmt="grid"
            ))
        case CheckType.MenuItems:
            print(f"running check type: {check_type}")
            items = missing_menuitem_data(DB_PATH)
            counts = [
                ("dish", len(items.with_missing_dish)),
                ("page", len(items.with_missing_page))
            ]
            headers = ["what type of relation is missing", "number missing"]
            print(tabulate(
                tabular_data=counts,
                headers=headers,
                tablefmt="grid"
            ))

        case _:
            print(f"unsupported check type {check_type}")
    return 0
