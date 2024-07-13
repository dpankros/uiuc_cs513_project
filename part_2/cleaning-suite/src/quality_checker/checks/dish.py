import sqlite3
from quality_checker.db import run_query
from quality_checker.models.dish import dish_factory
from tabulate import tabulate


def check_dish(conn: sqlite3.Connection) -> str:
    metrics = [
        (
            "Dish.times_appeared < 0",
            "select * from Dish as D where D.times_appeared < 0",
        ),
        (
            "Dish.first_appeared <= 0",
            "select * from Dish as D where D.first_appeared <= 0",
        ),
        (
            "Dish.last_appeared <= 0",
            "select * from Dish as D where D.last_appeared <= 0",
        ),
        (
            "Dish.first_appeared > Dish.last_appeared",
            "select * from Dish as D where D.first_appeared > D.last_appeared",
        ),
        (
            "Dish.lowest_price == NULL",
            "select * from Dish as D where D.lowest_price is NULL",
        ),
        (
            "Dish.highest_price == NULL",
            "select * from Dish as D where D.highest_price is NULL",
        ),
    ]
    data = [
        (name, len(run_query(conn, query=query, row_factory=dish_factory)))
        for (name, query) in metrics
    ]

    return tabulate(tabular_data=data, headers=["Metric", "value"], tablefmt="grid")
