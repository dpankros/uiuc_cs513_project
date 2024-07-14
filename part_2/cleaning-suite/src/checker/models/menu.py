from checker.db import RowFactory
from dataclasses import dataclass, fields
from typing import Any
import aiosqlite
from checker.models import Model, insert_entry


@dataclass
class Menu(Model):
    id: str
    name: str | None = None
    sponsor: str | None = None
    event: str | None = None
    venue: str | None = None
    place: str | None = None
    physical_description: str | None = None
    occasion: str | None = None
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
    occasion: str | None = None


def create_menu_factory(*, strict: bool) -> RowFactory[Menu]:
    def strict_factory(row_dict: dict[str | Any, Any]):
        return Menu(**row_dict)

    def lenient_factory(row_dict: dict[str | Any, Any]):
        dataclass_fields = {f.name for f in fields(Menu)}
        row_data = {column: value for column, value in row_dict.items()}
        filtered_data = {k: v for k, v in row_data.items() if k in dataclass_fields}
        return Menu(**filtered_data)

    return strict_factory if strict else lenient_factory

_TABLE_NAME = "Menu"

async def create_menu_table(conn: aiosqlite.Connection) -> None:
    query = f"""
    CREATE TABLE "{_TABLE_NAME}"
    (
        id                   integer constraint Menu_pk primary key,
        name                 text,
        sponsor              text,
        event                text,
        venue                text,
        place                text,
        physical_description text,
        occasion             text,
        notes                text,
        call_number          text,
        keywords             text,
        language             text,
        date                 text,
        location             text,
        location_type        text,
        currency             text,
        currency_symbol      text,
        status               text,
        page_count           int,
        dish_count           text
    )
    """
    await conn.execute(query)
    await conn.commit()

async def insert_menu(conn: aiosqlite.Connection, menu: Menu) -> None:
    await insert_entry(_TABLE_NAME, conn, menu)
