import functools

import pandas as pd

from importer2.ic import All, Unique, GreaterThan, IsUndefined, Any, IsValidForeignKey, IsFloat
from .cs513_report_task import CS513ReportTask


class MenuItemReportTask(CS513ReportTask):
  name = "Menu Item IC Violation Report Task"
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
