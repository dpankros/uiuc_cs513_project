from sqlalchemy import text
from sqlalchemy.engine import Connection


def constrain_to_range(low_range, high_range):
    # curried to provide necessary functionality
    def set_to_range_inner(col_name: str, col_value, ctx: dict):
        table_name = ctx.get('table_name')
        pk = ctx.get('primary_key')
        pk_col = ctx.get('primary_key_col', 'id')
        conn: Connection = ctx.get('connection')

        needs_update = False
        if col_value > high_range:
            col_value = high_range
            needs_update = True
        elif col_value < low_range:
            col_value = low_range
            needs_update = True

        if needs_update:
            update_sql = f"UPDATE {table_name} set {col_name} = {col_value} WHERE {pk_col} = {pk}"
            conn.execute(text(update_sql))
            conn.commit()

    return set_to_range_inner
