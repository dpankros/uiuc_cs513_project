from .cs513_sql_task import CS513SqlTask
from .cs513_verification_task import CS513VerificationTask


class MenuVerificationTask(CS513VerificationTask, CS513SqlTask):
  name = "Menu Verification"
  column_mapping = {
    # base_col: view_col
    "id": "id",
    "norm_name": "name",
    "norm_sponsor": "sponsor",
    "norm_event": "event",
    "norm_venue": "venue",
    "norm_place": "place",
    "norm_physical_description": "physical_description",
    "norm_occasion": "occasion",
    "norm_notes": "notes",
    "call_number": "call_number",
    "date": "date",
    "norm_location": "location",
    "currency": "currency",
    "currency_symbol": "currency_symbol",
    "status": "status",
    "page_count": "page_count",
    "dish_count": "dish_count",
  }
  base_table = "menu"
  verification_table = "_menu"
