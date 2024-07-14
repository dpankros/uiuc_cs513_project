from dataclasses import dataclass, fields
from typing import Any
from checker.db import RowFactory


@dataclass
class MenuPage:
    id: str
    menu_id: int
    page_number: int
    image_id: int
    full_height: int
    full_width: int
    uuid: str
    name: str | None

def create_menu_page_factory(*, strict: bool = True) -> RowFactory[MenuPage]:

    def strict_factory(row_dict: dict[str | Any, Any]) -> MenuPage:
        return MenuPage(**row_dict)

    def lenient_factory(row_dict: dict[str | Any, Any]):
        dataclass_fields = {f.name for f in fields(MenuPage)}
        row_data = {column: value for column, value in row_dict.items()}
        filtered_data = {k: v for k, v in row_data.items() if k in dataclass_fields}
        return MenuPage(**filtered_data)

    return strict_factory if strict else lenient_factory

