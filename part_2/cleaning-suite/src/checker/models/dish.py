from dataclasses import dataclass
import aiosqlite
from typing import Any
from checker.models import Model, insert_entry


@dataclass
class Dish(Model):
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

_TABLE_NAME = "Dish"

async def create_dish_table(conn: aiosqlite.Connection):
    query = f"""
    CREATE TABLE "{_TABLE_NAME}"
    (
        id             integer constraint Dish_pk primary key,
        name           text,
        description    text,
        menus_appeared int,
        times_appeared int,
        first_appeared int,
        last_appeared  int,
        lowest_price   real,
        highest_price  real
    )
    """
    await conn.execute(query)
    await conn.commit()

async def insert_dish(conn: aiosqlite.Connection, dish: Dish) -> None:
    await insert_entry(_TABLE_NAME, conn, dish)
