from sqlalchemy import text

from importer2.task import SqlTask


class CS513VerificationTask(SqlTask):
  column_mapping = {
    # base_col: view_col
    "id": "id",
  }
  base_table = None
  verification_table = None
  base_table_pk = "id"
  verification_table_pk = "id"

  def __init__(self, operation_config: dict = {}):
    super().__init__(operation_config)
    self.max_count: Engine = operation_config['max_count'] if 'max_count' in operation_config else None
    # self.sql_table: str = operation_config['sql_table'] if 'sql_table' in operation_config else None

  def run(self):
    super().run()

    self.max_count = self.max_count or 10

    has_errors = False
    error_count = 0

    try:
      with self.connection as conn:
        b_cursor = conn.execute(text(
          f"select {', '.join(self.column_mapping.keys())} from {self.base_table} order by {self.base_table_pk} asc;"))
        v_cursor = conn.execute(text(
          f"select {', '.join(self.column_mapping.values())} from {self.verification_table} order by {self.verification_table_pk} asc;"))

        b_cols = [*self.column_mapping.keys()]
        v_cols = [*self.column_mapping.values()]

        for row_num, b_row in enumerate(b_cursor):
          v_row = v_cursor.fetchone()
          deltas = []

          for col_num in range(len(self.column_mapping.keys())):
            b_col = b_cols[col_num]
            v_col = v_cols[col_num]
            if b_row[col_num] != v_row[col_num]:
              deltas.append(f"{self.base_table}.{b_col} ({b_row[col_num]}) != {self.verification_table}.{v_col} ({v_row[col_num]})")

          if len(deltas) > 0:
            error_count += 1
            has_errors = True

          if error_count < self.max_count and len(deltas) > 0:
            print(f"  - {b_cols[0]} == {b_row[0]}) {'; '.join(deltas)}")

    finally:
      self.connection.close()
      if has_errors:
        print(f"  {self.name} failed with {error_count} errors.")
      else:
        print(f"  {self.name} succeeded.")
