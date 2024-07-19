from sqlalchemy import text

from .cs513_ic_cleanup_task import Cs513IcCleanupTask


class MenuItemIcCleanupTask(Cs513IcCleanupTask):
  """
  Removes rows that create IC violations
  """
  name = "Menu Item IC Cleanup Task"

  foreign_keys = {
    "menu_page_id": "menu_page",
    "dish_id": "dish",
  }
