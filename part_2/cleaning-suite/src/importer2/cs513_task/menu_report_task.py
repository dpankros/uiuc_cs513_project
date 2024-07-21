from .cs513_report_task import CS513ReportTask


class MenuReportTask(CS513ReportTask):
    name = "Menu Report Task"
    base_table = "menu_orig"
    comparison_table = "_menu"
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
        # base_col: view_col
        "id": "id",
        "name": "name",
        "sponsor": "sponsor",
        "event": "event",
        "venue": "venue",
        "place": "place",
        "physical_description": "physical_description",
        "occasion": "occasion",
        "notes": "notes",
        "call_number": "call_number",
        "date": "date",
        "location": "location",
        "currency": "currency",
        "currency_symbol": "currency_symbol",
        "status": "status",
        "page_count": "page_count",
        "dish_count": "dish_count",
    }

    stat_columns = {
        "name": {},
        "sponsor": {},
        "event": {},
        "venue": {},
        "place": { "type": "multi_valued_stats"},
        "physical_description":  { "type": "multi_valued_stats"},
        "occasion": { "type": "multi_valued_stats"},
        "notes": { "type": "multi_valued_stats"},
        "call_number": {},
        "date": {},
        "location": {},
        "currency": {},
        "currency_symbol": {},
        "status": {},
    }
