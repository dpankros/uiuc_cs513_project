from importer2.ic import All, Any, Unique, GreaterThan, IsUndefined, IsValidForeignKey
from .cs513_report_task import CS513ReportTask


class MenuPageReportTask(CS513ReportTask):
  name = "Menu Page IC Violation Report Task"
  base_table = "menu_page_orig"
  comparison_table = "menu_page"
  foreign_keys = {
    "menu_id": "menu",
  }

  integrity_constraints = {
    "id": All(Unique(), GreaterThan(0)),
    "menu_id": Any(IsUndefined(), IsValidForeignKey('menu')),
    "page_number": Any(IsUndefined(), GreaterThan(0)),
    "full_height": GreaterThan(0),
    "full_width": GreaterThan(0),
  }
