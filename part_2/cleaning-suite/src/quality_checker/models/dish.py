from dataclasses import dataclass
import sqlite3


@dataclass
class Dish:
    id: int
    name: str
    description: str
    menus_appeared: int
    times_appeared: int
    first_appeared: int
    last_appeared: int
    lowest_price: float
    highest_price: float


def dish_factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> Dish:
    fields = [column[0] for column in cursor.description]
    return Dish(**{k: v for k, v in zip(fields, row)})
