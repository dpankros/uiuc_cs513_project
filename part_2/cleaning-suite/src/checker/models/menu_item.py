from dataclasses import dataclass, field
from typing import Any
from checker.models import Model


@dataclass
class MenuItem(Model):
    id: str
    menu_page_id: str
    price: int
    high_price: int
    dish_id: int
    created_at: int
    updated_at: int
    xpos: int
    ypos: int
    menu_id: int | None = None
    page_number: int | None = None
    image_id: int | None = None
    full_height: int | None = None
    full_width: int | None = None
    uuid: str | None = None
    name: str | None = None
    description: str | None = None
    menus_appeared: list[int] = field(default_factory=list)
    times_appeared: int | None = None
    first_appeared: int | None = None
    last_appeared: int | None = None
    lowest_price: int | None = None
    highest_price: int | None = None


def menu_item_factory(row_dict: dict[str | Any, Any]) -> MenuItem:
    return MenuItem(**row_dict)
