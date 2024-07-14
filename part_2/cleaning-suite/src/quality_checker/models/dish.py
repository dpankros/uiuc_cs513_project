from dataclasses import dataclass
import sqlite3
from typing import Any


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


def dish_factory(row_dict: dict[str, Any]) -> Dish:
    return Dish(**row_dict)
