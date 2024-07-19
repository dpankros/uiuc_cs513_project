from .cs513_sql_task import CS513SqlTask
from .cs513_verification_task import CS513VerificationTask


class MenuItemVerificationTask(CS513VerificationTask, CS513SqlTask):

  name = "Menu Item Verification"
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

  base_table = "menu_item"
  verification_table = "menu_item"
