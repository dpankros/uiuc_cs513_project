from .cs513_report_task import CS513ReportTask


class DishReportTask(CS513ReportTask):
    name = "Dish Report Task"
    base_table = "dish_orig"
    comparison_table = "_dish"
    # foreign_keys = {
    #     "menu_page_id": "menu_page",
    #     "dish_id": "dish",
    # }
    #
    # integrity_constraints = {
    #     "id": All(Unique(), GreaterThan(0)),
    #     "menu_page_id": Any(IsUndefined(), IsValidForeignKey('menu_page')),
    #     "price": Any(GreaterThan(0), IsUndefined()),
    #     "dish_id": Any(IsUndefined(), IsValidForeignKey('dish')),
    #     # "created_at": should be in iso8601 format.  Must be defined.  Must be <= NOW
    #     # "updated_at": should be in iso8601 format Must be <= NOW
    #     "xpos": IsFloat(),
    #     "ypos": IsFloat(),
    # }

    column_mapping = {
        "id": "id",
        "name": "name",
        "description": "description",
        "menus_appeared": "menus_appeared",
        "times_appeared": "times_appeared",
        "first_appeared": "first_appeared",
        "last_appeared": "last_appeared",
        "lowest_price": "lowest_price",
        "highest_price": "highest_price",
    }

    stat_columns = {
        "name": { "type": "standard_stats"},
        "description": {},
        "menus_appeared": { "type": "numeric_stats" },
        "times_appeared": { "type": "numeric_stats" },
        "first_appeared": { "type": "numeric_stats" },
        "last_appeared": { "type": "numeric_stats" },
        "lowest_price": { "type": "numeric_stats" },
        "highest_price": { "type": "numeric_stats" },
    }
