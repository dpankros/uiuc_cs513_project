import sqlite3
from dataclasses import dataclass


@dataclass
class MenuPage:
    id: str
    menu_id: int
    page_number: int
    image_id: int
    full_height: int
    full_width: int
    uuid: str
    name: str
    sponsor: str
    event: str
    venue: str
    place: str
    physical_description: str
    occasion: str
    notes: str
    call_number: str
    keywords: list[str]
    language: str
    date: str
    location: str
    location_type: str
    currency: str
    currency_symbol: str
    status: str
    page_count: int
    dish_count: int
    
    


def menu_page_factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> MenuPage:
    fields = [column[0] for column in cursor.description]
    return MenuPage(**{k: v for k, v in zip(fields, row)})
