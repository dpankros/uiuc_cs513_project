import time
import asyncio
import aiosqlite
from os.path import join
from checker.models.dish import create_dish_table, dish_factory, insert_dish
from checker.models.menu import create_menu_factory, create_menu_table, insert_menu
from checker.models.menu_item import create_menu_item_table, insert_menu_item, menu_item_factory
from importer.do_import import do_import
import click

_DATA_PREFIX = join("..", "..", "data")
_DISH = join(_DATA_PREFIX, "Dish.csv")
_MENU = join(_DATA_PREFIX, "Menu.csv")
_MENU_ITEM = join(_DATA_PREFIX, "MenuItem.csv")
_MENU_PAGE = join(_DATA_PREFIX, "MenuPage.csv")

_DEFAULT_DB_FILE = join("..", "..", "imports", f"data-import.{time.time()}.sqlite")


@click.command()
@click.option(
    "--db-file",
    default=_DEFAULT_DB_FILE,
    help="The DB file to which to import CSV data (defaults to a timestamped DB file)",
)
def main(db_file: str) -> int:
    return asyncio.run(run(db_file))


async def run(db_file: str) -> int:
    loaders = {
        "dish": (_DISH, import_dishes),
        "menu": (_MENU, import_menus),
        "menu_item": (_MENU_ITEM, import_menu_items),
        # "menu_page": (_MENU_PAGE, import_menu_pages),
    }
    print(f"creating new SQLite file {db_file}")
    async with aiosqlite.connect(db_file) as conn:
        for entity_name, (filename, importer) in loaders.items():
            print(f"-----{entity_name}-----")
            await importer(filename, conn)

    return 0

async def import_menus(filename: str, conn: aiosqlite.Connection) -> int:
    return await do_import(
        filename,
        conn=conn,
        row_factory=create_menu_factory(strict=False),
        table_creator=create_menu_table,
        inserter=insert_menu,
    )

async def import_dishes(filename: str, conn: aiosqlite.Connection) -> int:
    return await do_import(
        filename,
        conn=conn,
        row_factory=dish_factory,
        table_creator=create_dish_table,
        inserter=insert_dish,
    )

async def import_menu_items(filename: str, conn: aiosqlite.Connection) -> int:
    return await do_import(
        filename,
        conn=conn,
        row_factory=menu_item_factory,
        table_creator=create_menu_item_table,
        inserter=insert_menu_item,
    )
