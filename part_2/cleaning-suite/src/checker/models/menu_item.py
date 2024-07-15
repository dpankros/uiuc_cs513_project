from dataclasses import dataclass, field
from typing import Any
import aiosqlite
from checker.models import Model, insert_entry


@dataclass
class MenuItem(Model):
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


def menu_item_factory(row_dict: dict[str | Any, Any]) -> MenuItem:
    return MenuItem(**row_dict)


_TABLE_NAME = "MenuItem"


async def create_menu_item_table(conn: aiosqlite.Connection) -> None:
    query = f"""
    CREATE TABLE "{_TABLE_NAME}"
    (
        id           integer constraint MenuItem_pk primary key,
        menu_page_id integer constraint MenuItem_MenuPage_id_fk references MenuPage,
        price        real,
        high_price   real,
        dish_id      integer constraint MenuItem_Dish_id_fk references Dish,
        created_at   text,
        updated_at   text,
        xpos         real,
        ypos         text
    )
    """
    await conn.execute(query)
    await conn.commit()


async def insert_menu_item(conn: aiosqlite.Connection, menu_item: MenuItem):
    await insert_entry(_TABLE_NAME, conn, menu_item)
