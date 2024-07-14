import sqlite3
from checker.db import run_query
from checker.models.dish import dish_factory
from checker.checks import CheckResult


def check_dish(conn: sqlite3.Connection) -> CheckResult:
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
    return [
        (name, len(run_query(conn, query=query, row_factory=dish_factory)))
        for (name, query) in metrics
    ]
