from dataclasses import dataclass, field
import sqlite3


@dataclass
class MenuItem:
    id: str
    menu_page_id: str
    price: int
    high_price: int
    dish_id: int
    created_at: int
    updated_at: int
    xpos: int
    ypos: int
    menu_id: int | None = None
    page_number: int | None = None
    image_id: int | None = None
    full_height: int | None = None
    full_width: int | None = None
    uuid: str | None = None
    name: str | None = None
    description: str | None = None
    menus_appeared: list[int] = field(default_factory=list)
    times_appeared: int | None = None
    first_appeared: int | None = None
    last_appeared: int | None = None
    lowest_price: int | None = None
    highest_price: int | None = None


def menu_item_factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> MenuItem:
    fields = [column[0] for column in cursor.description]
    return MenuItem(**{k: v for k, v in zip(fields, row)})
