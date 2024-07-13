import click
from enum import StrEnum
from tabulate import tabulate

from quality_checker.sqlite import get_table_counts


class CheckType(StrEnum):
    TableCounts = "table_counts"


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
            counts = get_table_counts("../../data.sqlite")
            print("counts")
            print(tabulate(
                tabular_data=counts,
                headers=["table", "count"],
                tablefmt="grid"
            ))
        case _:
            print(f"unsupported check type {check_type}")
    return 0
