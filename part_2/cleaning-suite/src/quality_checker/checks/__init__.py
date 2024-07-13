import sqlite3
from typing import Callable
from tabulate import tabulate

type CheckResult = list[tuple[str, float]]

type Check = tuple[str, Callable[[sqlite3.Connection], CheckResult]]
type CheckFormatter = Callable[[CheckResult], str]

def tabulate_check_formatter(data: CheckResult) -> str:
    return tabulate(
        tabular_data=data,
        headers=["Metric", "Value"],
        tablefmt="grid",
    )
