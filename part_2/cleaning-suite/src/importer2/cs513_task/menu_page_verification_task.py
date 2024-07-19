from .cs513_sql_task import CS513SqlTask
from .cs513_verification_task import CS513VerificationTask


class MenuPageVerificationTask(CS513VerificationTask, CS513SqlTask):
  name = "Menu Page Verification"

  column_mapping = {
    # base_col: view_col
    "id": "id",
    "menu_id": "menu_id",
    "page_number": "page_number",
    "image_id": "image_id",
    "full_height": "full_height",
    "full_width": "full_width",
    "uuid": "uuid",
  }
  base_table = "menu_page"
  verification_table = "menu_page"


