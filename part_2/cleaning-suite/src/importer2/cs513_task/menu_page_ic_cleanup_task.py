from sqlalchemy import text

from .cs513_ic_cleanup_task import Cs513IcCleanupTask


class MenuPageIcCleanupTask(Cs513IcCleanupTask):
  """
  Removes rows that create IC violations
  """
  name = "Menu Page IC Cleanup Task"

  foreign_keys = {
    "menu_id": "menu",
  }
