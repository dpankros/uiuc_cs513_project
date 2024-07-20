from .cleaner import set_to_null, constrain_to_min
from importer2.ic import All, Unique, GreaterThan, IsUndefined, Any, IsValidForeignKey
from .cs513_ic_task import CS513IcTask


class MenuPageIcTask(CS513IcTask):
    name = "Menu Page IC Violation Report Task"
    pk = 'id'

    integrity_constraints = {
        "id": All(Unique(), GreaterThan(0)),
        "menu_id": (
            Any(IsUndefined(), IsValidForeignKey('menu')),
            set_to_null,
        ),
        "page_number": (
            Any(IsUndefined(), GreaterThan(0)),
            set_to_null
        ),
        "full_height": (
            Any(IsUndefined(), GreaterThan(0)),
            set_to_null
        ),
        "full_width": (
            Any(IsUndefined(), GreaterThan(0)),
            set_to_null
        )
    }
