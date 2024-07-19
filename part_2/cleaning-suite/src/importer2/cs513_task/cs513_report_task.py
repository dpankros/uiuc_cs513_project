import functools

import pandas as pd

from importer2.task import SqlTask


class CS513ReportTask(SqlTask):
  column_mapping = {
    # base_col: view_col
    "id": "id",
  }
  base_table = None
  comparison_table = None
  base_table_pk = "id"
  comparison_table_pk = "id"

  # column: [ constraint, constraint...] OR
  # column: constraint
  integrity_constraints = {}
  # the foreign keys from the base table.
  # key: foreign_table
  foreign_keys = {}

  def __init__(self, operation_config: dict = {}):
    super().__init__(operation_config)
    self.max_count: Engine = operation_config.get('max_count', 10)
    self.table = operation_config.get('table', None)
    if 'name' in operation_config: # ONLY set if if is defined in the config
      self.name = operation_config.get('name')

  def run(self):
    self.connection: Connection = self.sql_engine.connect()

    all_violations = {}
    violation_cols = {}
    try:
      with self.connection as conn:
        data = pd.read_sql(f"select {', '.join(self.integrity_constraints.keys())} from {self.table}", conn)

        for index, row in data.iterrows():
          for col_index, col in enumerate(data.columns):
            constraint = self.integrity_constraints[col]
            violations = constraint.check(
              col, # column name
              getattr(row, col), # colum value
              { # context object
                "row": row,
                "table_name": self.table,
                "connection": conn,
                "data": data,
                "foreign_table": self.foreign_keys.get(col, None)
              }
            )
            if violations is not None:
              all_violations[index] = violations
              violation_cols[col] = violation_cols.get(col, 0) + 1


      print(f"  {len(all_violations.keys())} Rows with IC violations")
      if len(all_violations.keys()) > 0:
        cols_strs = []
        for key, count in violation_cols.items():
          cols_strs.append(f"{key} ({count})")
        print(f"  Errors were detected in the following columns: {', '.join(cols_strs)}")
    finally:
      self.connection.close()
