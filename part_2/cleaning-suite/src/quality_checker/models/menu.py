import sqlite3
from dataclasses import dataclass, fields
from typing import Callable


@dataclass
class Menu:
    id: str
    name: str | None = None
    sponsor: str | None = None
    event: str | None = None
    venue: str | None = None
    place: str | None = None
    physical_description: str | None = None
    occassion: str | None = None
    notes: str | None = None
    call_number: str | None = None
    keywords: str | None = None
    language: str | None = None
    date: str | None = None
    location: str | None = None
    location_type: str | None = None
    currency: str | None = None
    currency_symbol: str | None = None
    status: str | None = None
    page_count: int | None = None
    dish_count: int | None = None


def create_menu_factory(
    *, strict: bool
) -> Callable[[sqlite3.Cursor, sqlite3.Row], Menu]:
    def strict_factory(cursor: sqlite3.Cursor, row: sqlite3.Row):
        fields = [column[0] for column in cursor.description]
        return Menu(**{k: v for k, v in zip(fields, row)})

    def lenient_factory(cursor: sqlite3.Cursor, row: sqlite3.Row):
        dataclass_fields = {f.name for f in fields(Menu)}
        row_data = {
            column: value
            for column, value in zip([column[0] for column in cursor.description], row)
        }
        filtered_data = {k: v for k, v in row_data.items() if k in dataclass_fields}
        return Menu(**filtered_data)

    return strict_factory if strict else lenient_factory
