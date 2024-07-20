from sqlalchemy import text
from sqlalchemy.engine import Connection


def constrain_to_max(max_value):
    # curried to provide necessary functionality
    def constrain_to_max_inner(col_name: str, col_value, ctx: dict):
        table_name = ctx.get('table_name')
        pk = ctx.get('primary_key')
        pk_col = ctx.get('primary_key_col', 'id')
        conn: Connection = ctx.get('connection')

        if col_value > max_value:
            update_sql = f"UPDATE {table_name} set {col_name} = {max_value} WHERE {pk_col} = {pk}"
            conn.execute(text(update_sql))
            conn.commit()

    return set_to_between_inner
