import sqlite3
from dataclasses import dataclass


@dataclass
class Menu:
    id: str


def menu_factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> Menu:
    fields = [column[0] for column in cursor.description]
    return Menu(**{k: v for k, v in zip(fields, row)})
