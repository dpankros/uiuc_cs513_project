from sqlalchemy import text
from sqlalchemy.engine import Connection


def set_to_value(value):

    def set_to_value_inner(col_name: str, col_value, ctx: dict):
        table_name = ctx.get('table_name')
        pk = ctx.get('primary_key')
        pk_col = ctx.get('primary_key_col', 'id')
        conn: Connection = ctx.get('connection')

        update_sql = f"UPDATE {table_name} set {col_name} = {value} WHERE {pk_col} = {pk}"
        conn.execute(text(update_sql))
        conn.commit()
    return set_to_value_inner
