from importer2.ic import All, Unique, GreaterThan, IsUndefined, Any, IsValidForeignKey, IsFloat
from .cs513_report_task import CS513ReportTask


class MenuItemReportTask(CS513ReportTask):
    name = "Menu Item Report Task"
    base_table = "menu_item_orig"
    comparison_table = "menu_item"
    foreign_keys = {
        "menu_page_id": "menu_page",
        "dish_id": "dish",
    }

    integrity_constraints = {
        "id": All(Unique(), GreaterThan(0)),
        "menu_page_id": Any(IsUndefined(), IsValidForeignKey('menu_page')),
        "price": Any(GreaterThan(0), IsUndefined()),
        "dish_id": Any(IsUndefined(), IsValidForeignKey('dish')),
        # "created_at": should be in iso8601 format.  Must be defined.  Must be <= NOW
        # "updated_at": should be in iso8601 format Must be <= NOW
        "xpos": IsFloat(),
        "ypos": IsFloat(),
    }

    column_mapping = {
        # base_col: view_col
        "id": "id",
        "menu_page_id": "menu_page_id",
        "price": "price",
        "high_price": "high_price",
        "dish_id": "dish_id",
        "created_at": "created_at",
        "updated_at": "updated_at",
        "xpos": "xpos",
        "ypos": "ypos",
    }

    stat_columns = {
        "price": {"type": "numeric_stats"},
        "high_price": {"type": "numeric_stats"},
        "xpos": {"type": "numeric_stats"},
        "ypos": {"type": "numeric_stats"},
        "menu_page_id": {"type": "fk_stats"},
        "dish_id": {"type": "fk_stats"},
        
    }
