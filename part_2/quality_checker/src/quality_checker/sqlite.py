from dataclasses import dataclass
import sqlite3
from typing import Callable
from quality_checker.models.menu_item import MenuItem, menu_item_factory

type RowFactory[T] = Callable[[sqlite3.Cursor, sqlite3.Row], T]


@dataclass
class MenuItemMissingPieces:
    with_missing_page: list[MenuItem]
    with_missing_dish: list[MenuItem]


def _run_query[T](
    db_path: str,
    *,
    query: str,
    row_factory: RowFactory[T],
) -> list[T]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = row_factory
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def get_table_counts(db_path: str) -> list[tuple[str, int]]:
    query = """
    select 'MenuItem', count(*) from MenuItem MI
    union
    select 'Dish', count(*) from Dish D
    union
    select 'Menu', count(*) from Menu M
    union
    select 'MenuPage', count(*) from MenuPage MP;
    """

    def table_counts_factory(
        cursor: sqlite3.Cursor,
        row: sqlite3.Row,
    ) -> tuple[str, int]:
        return row[0], row[1]
    return _run_query(db_path, query=query, row_factory=table_counts_factory)


def missing_menuitem_data(db_path: str) -> MenuItemMissingPieces:
    missing_pages_query: str = """select * from MenuItem MI
    left outer join main.MenuPage MP on MI.menu_page_id = MP.id
    where MP.id is null;
    """
    with_missing_page = _run_query(
        db_path,
        query=missing_pages_query,
        row_factory=menu_item_factory
    )

    missing_dishes_query: str = """
    select * from MenuItem MI
    left outer join main.Dish D on MI.dish_id = D.id
    where D.id is null;
    """
    with_missing_dish = _run_query(
        db_path,
        query=missing_dishes_query,
        row_factory=menu_item_factory,
    )
    return MenuItemMissingPieces(
        with_missing_page=with_missing_page,
        with_missing_dish=with_missing_dish
    )
