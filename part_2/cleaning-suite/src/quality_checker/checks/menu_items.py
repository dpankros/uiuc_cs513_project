from dataclasses import dataclass
import sqlite3
from quality_checker.db import run_query
from quality_checker.models.menu_item import MenuItem, menu_item_factory
from quality_checker.checks import CheckResult


@dataclass
class MenuItemMissingPieces:
    with_missing_page: list[MenuItem]
    with_missing_dish: list[MenuItem]


def check_menu_items(conn: sqlite3.Connection) -> CheckResult:
    items = _missing_menuitem_data(conn)
    return [
        ("MenuItem -> Dish FK violations", len(items.with_missing_dish)),
        ("MenuItem -> Page FK violations", len(items.with_missing_page)),
    ]


def _missing_menuitem_data(conn: sqlite3.Connection) -> MenuItemMissingPieces:
    missing_pages_query: str = """select * from MenuItem MI
    left outer join main.MenuPage MP on MI.menu_page_id = MP.id
    where MP.id is null;
    """
    with_missing_page = run_query(
        conn, query=missing_pages_query, row_factory=menu_item_factory
    )

    missing_dishes_query: str = """
    select * from MenuItem MI
    left outer join main.Dish D on MI.dish_id = D.id
    where D.id is null;
    """
    with_missing_dish = run_query(
        conn,
        query=missing_dishes_query,
        row_factory=menu_item_factory,
    )
    return MenuItemMissingPieces(
        with_missing_page=with_missing_page, with_missing_dish=with_missing_dish
    )
