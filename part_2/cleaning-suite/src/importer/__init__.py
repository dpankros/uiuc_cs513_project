import csv
from os.path import join
from checker.db import RowFactory
from checker.models.menu import create_menu_factory
from checker.models.dish import dish_factory
from checker.models.menu_item import menu_item_factory
from checker.models.menu_page import create_menu_page_factory

_DATA_PREFIX = join("..", "..", "data")
_DISH = join(_DATA_PREFIX, "Dish.csv")
_MENU = join(_DATA_PREFIX, "Menu.csv")
_MENU_ITEM = join(_DATA_PREFIX, "MenuItem.csv")
_MENU_PAGE = join(_DATA_PREFIX, "MenuPage.csv")


def main() -> int:
    loaders = {
        _DISH: dish_factory,
        _MENU: create_menu_factory(strict=False),
        _MENU_ITEM: menu_item_factory,
        _MENU_PAGE:create_menu_page_factory(strict=False)
    }
    for filename, factory in loaders.items():
        read_csv(filename, row_factory=factory)

    return 0


def read_csv[T](filename: str, *, row_factory: RowFactory[T]) -> list[T]:
    print(f"loading from {filename}")
    with open(filename, "r") as f:
        rdr = csv.DictReader(f, delimiter=",")
        vals: list[T] = []
        for idx, row in enumerate(rdr):
            try:
                val = row_factory(row)
                vals.append(val)
            except Exception as e:
                print(f"couldn't load item {idx+1}: {e}")
                raise
        print(f"loaded {len(vals)} from {filename}")
        return vals
