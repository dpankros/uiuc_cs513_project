from .cleaner import set_to_null, constrain_to_range
from importer2.ic import All, Unique, GreaterThan, IsUndefined, Any, IsValidForeignKey, IsFloat
from .cs513_ic_task import CS513IcTask


class MenuItemIcTask(CS513IcTask):
    name = "Menu Item IC Violation Report Task"
    pk = 'id'

    integrity_constraints = {
        "id": All(Unique(), GreaterThan(0)),  # no corrections
        "menu_page_id": (
            Any(IsUndefined(), IsValidForeignKey('menu_page')),
            set_to_null
        ),
        "price": (
            Any(IsUndefined(), GreaterThan(0)),
            set_to_null
        ),
        "high_price": (
            Any(IsUndefined(), GreaterThan(0)),
            set_to_null
        ),
        "dish_id": (
            Any(IsUndefined(), IsValidForeignKey('dish')),
            set_to_null
        ),
        # "created_at": should be in iso8601 format.  Must be defined.  Must be <= NOW
        # "updated_at": should be in iso8601 format Must be <= NOW
        "xpos": (
            IsFloat(),
            constrain_to_range(0.0, 1.0),
        ),
        "ypos": (
            IsFloat(),
            constrain_to_range(0.0, 1.0),
        ),
    }
