from dataclasses import dataclass
import sqlite3
from tabulate import tabulate
from quality_checker.models.menu import create_menu_factory, Menu
from quality_checker.db import run_query


@dataclass
class CheckMenusResult:
    differing_page_count: list[Menu]
    differing_num_dishes: list[Menu]


def check_menus(conn: sqlite3.Connection) -> str:
    page_count_differs_from_menu_page = run_query(
        conn,
        query="""
        select M.id, count(MP.id), M.page_count from Menu M
        left join main.MenuPage MP on M.id = MP.menu_id
        group by M.id having count(MP.id) <> M.page_count;
        """,
        row_factory=create_menu_factory(strict=False),
    )

    dish_count_differs_from_num_dishes_in_menu_pages = run_query(
        conn,
        query="""
        select M.id, MP.page_number, M.page_count, count(D.id) as 'Dishes in DB', M.dish_count from Menu M
        left join main.MenuPage MP on M.id = MP.menu_id
        left join main.MenuItem MI on MP.id = MI.menu_page_id
        left join main.Dish D on MI.dish_id = D.id
        group by M.id having count(D.id) <> M.dish_count
        order by M.id asc, MP.page_number asc;
        """,
        row_factory=create_menu_factory(strict=False),
    )

    data = [
        ("Menu.page_count <> MenuPage.menu_id", len(page_count_differs_from_menu_page)),
        (
            "Menu.dish_count <> MenuItem.menu_page_id <> MenuPage.menu_id",
            len(dish_count_differs_from_num_dishes_in_menu_pages),
        ),
    ]

    return tabulate(
        tabular_data=data,
        headers=["Integrity constraint", "Number of violations"],
        tablefmt="grid",
    )

    return ""
