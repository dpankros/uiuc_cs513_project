from sqlalchemy import text

from .cs513_sql_task import CS513SqlTask

class Cs513IcCleanupTask(CS513SqlTask):
  def run(self):
    super().run()
    table_name = self.config.table

    def create_ic_select(base_table: str, foreign_key: str, foreign_table: str, foreign_pk: str = 'id'):
      return f"select b.id as id from {base_table} b left join {foreign_table} f on b.{foreign_key} = f.{foreign_pk} where f.{foreign_pk} is NULL"

    try:
      with self.connection as conn:
        while True:
          any_deleted = False
          for key, foreign_table in self.foreign_keys.items():
            violation_id_cursor = conn.execute(
              text(create_ic_select(table_name, key, foreign_table)))  # they all use id for keys
            violation_ids = {str(v[0]) for v in violation_id_cursor.fetchall()}
            if len(violation_ids) > 0:
              any_deleted = True

            conn.execute(
              text(f"DELETE FROM {table_name} WHERE id in ({','.join(violation_ids)})")
            )
            conn.commit()
          if not any_deleted:
              break
    finally:
      self.connection
