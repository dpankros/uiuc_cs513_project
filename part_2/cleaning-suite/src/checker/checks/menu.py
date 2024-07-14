from dataclasses import dataclass
import sqlite3
from checker.models.menu import create_menu_factory, Menu
from checker.db import run_query
from checker.checks import CheckResult


@dataclass
class CheckMenusResult:
    differing_page_count: list[Menu]
    differing_num_dishes: list[Menu]


def check_menus(conn: sqlite3.Connection) -> CheckResult:
    metrics = [
        (
            "Menu.page_count <> MenuPage.menu_id FK violations",
            """
            select M.id, count(MP.id), M.page_count from Menu M
            left join main.MenuPage MP on M.id = MP.menu_id
            group by M.id having count(MP.id) <> M.page_count;
            """,
            create_menu_factory(strict=False),
        ),
        (
            "Menu.dish_count <> MenuItem.menu_page_id <> MenuPage.menu_id FK violations",
            """
            select M.id, MP.page_number, M.page_count, count(D.id) as 'Dishes in DB', M.dish_count from Menu M
            left join main.MenuPage MP on M.id = MP.menu_id
            left join main.MenuItem MI on MP.id = MI.menu_page_id
            left join main.Dish D on MI.dish_id = D.id
            group by M.id having count(D.id) <> M.dish_count
            order by M.id asc, MP.page_number asc;
            """,
            create_menu_factory(strict=False),
        ),
        (
            "Menu.name is NULL",
            "select * from Menu as M where M.name is NULL",
            create_menu_factory(strict=False),
        ),
    ]
    return [
        (descr, len(run_query(conn, query=query, row_factory=factory)))
        for (descr, query, factory) in metrics
    ]
