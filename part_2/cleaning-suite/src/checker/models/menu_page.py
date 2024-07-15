from dataclasses import dataclass, fields
import aiosqlite
from typing import Any
from checker.db import RowFactory
from checker.models import Model, insert_entry


@dataclass
class MenuPage(Model):
    id: str
    menu_id: int
    page_number: int
    image_id: int
    full_height: int
    full_width: int
    uuid: str


def create_menu_page_factory(*, strict: bool = True) -> RowFactory[MenuPage]:
    def strict_factory(row_dict: dict[str | Any, Any]) -> MenuPage:
        return MenuPage(**row_dict)

    def lenient_factory(row_dict: dict[str | Any, Any]):
        dataclass_fields = {f.name for f in fields(MenuPage)}
        row_data = {column: value for column, value in row_dict.items()}
        filtered_data = {k: v for k, v in row_data.items() if k in dataclass_fields}
        return MenuPage(**filtered_data)

    return strict_factory if strict else lenient_factory


_TABLE_NAME = "MenuPage"


async def create_menu_page_table(conn: aiosqlite.Connection) -> None:
    query = f"""
    CREATE TABLE "{_TABLE_NAME}"
    (
        id          integer constraint MenuPage_pk primary key,
        menu_id     integer constraint MenuPage_Menu_id_fk references Menu,
        page_number integer,
        image_id    double,
        full_height integer,
        full_width  integer,
        uuid        text
    )
    """
    await conn.execute(query)
    await conn.commit()


async def insert_menu_page(conn: aiosqlite.Connection, menu_page: MenuPage):
    await insert_entry(_TABLE_NAME, conn, menu_page)
