import time
import asyncio
from typing import Awaitable
import aiosqlite
from os.path import join
from importer.menu import import_menus
from importer.dish import import_dishes
import click

_DATA_PREFIX = join("..", "..", "data")
_DISH = join(_DATA_PREFIX, "Dish.csv")
_MENU = join(_DATA_PREFIX, "Menu.csv")
_MENU_ITEM = join(_DATA_PREFIX, "MenuItem.csv")
_MENU_PAGE = join(_DATA_PREFIX, "MenuPage.csv")

@click.command()
@click.option(
    "--db-file", default=f"data-import.{time.time()}.sqlite", help="The DB file to which to import CSV data (defaults to a timestamped DB file)"
)
def main(db_file: str) -> int:
    asyncio.run(run(db_file))

async def run(db_file: str) -> int:
    loaders = {
        "dish": (_DISH, import_dishes),
        "menu": (_MENU, import_menus),
        # "menu_item": (_MENU_ITEM: import_menu_items),
        # "menu_page": (_MENU_PAGE, import_menu_pages),
    }
    print(f"creating new SQLite file {db_file}")
    async with aiosqlite.connect(db_file) as conn:
        for entity_name, (filename, importer) in loaders.items():
            print(f"-----{entity_name}-----")
            await importer(filename, conn)

    return 0

