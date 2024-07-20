from sqlalchemy import text
from sqlalchemy.engine import Connection

from importer2.ic import All, Unique, GreaterThan, IsUndefined, Any, IsValidForeignKey, IsFloat
from .cs513_ic_task import CS513IcTask


def set_column_to_null(col_name: str, col_value, ctx: dict):
  table_name = ctx.get('table_name')
  pk = ctx.get('primary_key')
  pk_col = ctx.get('primary_key_col', 'id')
  conn: Connection = ctx.get('connection')

  update_sql = f"UPDATE {table_name} set {col_name} = NULL WHERE {pk_col} = {pk}"
  conn.execute(text(update_sql))
  conn.commit()

class MenuItemIcTask(CS513IcTask):
  name = "Menu Item IC Violation Report Task"
  pk = 'id'

  integrity_constraints = {
    "id": All(Unique(), GreaterThan(0)),
    "menu_page_id": (
      Any(IsUndefined(), IsValidForeignKey('menu_page')),
      set_column_to_null
    ),
    "price": (
      Any(IsUndefined(), GreaterThan(0)),
      set_column_to_null
    ),
    "dish_id": (
      Any(IsUndefined(), IsValidForeignKey('dish')),
      set_column_to_null
    ),
    # "created_at": should be in iso8601 format.  Must be defined.  Must be <= NOW
    # "updated_at": should be in iso8601 format Must be <= NOW
    "xpos": IsFloat(),
    "ypos": IsFloat(),
  }

