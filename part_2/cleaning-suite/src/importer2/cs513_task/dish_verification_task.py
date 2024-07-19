

from .cs513_sql_task import CS513SqlTask
from .cs513_verification_task import CS513VerificationTask


class DishVerificationTask(CS513VerificationTask, CS513SqlTask):
  name = "Dish Verification"
  column_mapping = {
    # base_col: view_col
    "id": "id",
    "norm_name": "name",
    "description": "description",
    # "menus_appeared": "menus_appeared",
    "times_appeared": "times_appeared",
    "first_appeared": "first_appeared",
    "last_appeared": "last_appeared",
    # "lowest_price": "lowest_price",
    # "highest_price": "highest_price",
  }
  base_table = "dish"
  verification_table = "_dish"

