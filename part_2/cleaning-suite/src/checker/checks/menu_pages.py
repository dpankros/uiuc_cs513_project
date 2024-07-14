import sqlite3
from typing import Any
from checker.db import run_query
from checker.models.menu import Menu, create_menu_factory
from dataclasses import dataclass
from checker.models.menu_page import create_menu_page_factory, MenuPage
from checker.checks import CheckResult

@dataclass
class MenuAndMenuPage:
    menu: Menu
    menu_page: MenuPage

def menu_and_menu_page_factory(row_dict: dict[str | Any, Any]) -> MenuAndMenuPage:
    menu = create_menu_factory(strict=False)(row_dict)
    menu_page = create_menu_page_factory(strict=False)(row_dict)
    return MenuAndMenuPage(menu=menu, menu_page=menu_page)

def check_menu_pages(conn: sqlite3.Connection) -> CheckResult:
    query = """
    select * from MenuPage MP
    left outer join main.Menu M on M.id = MP.menu_id
    where M.id is NULL;
    """
    broken_foreign_keys = run_query(conn, query=query, row_factory=menu_and_menu_page_factory)
    distinct_uuids = run_query(
        conn,
        query="select distinct uuid from MenuPage order by uuid asc;",
        row_factory=lambda row_dict: list(row_dict.values())[0],
    )
    total_menus = run_query(
        conn,
        query="select MP.id from MenuPage MP",
        row_factory=lambda row_dict: list(row_dict.values())[0],
    )
    return [
        ("Duplicate UUIDs", len(total_menus) - len(distinct_uuids)),
        ("Menu.id <> MenuPage.menu_id FK violations", len(broken_foreign_keys)),
    ]
