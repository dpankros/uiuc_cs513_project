import pandas as pd

from importer2.task import SqlTask
from sqlalchemy.engine import Connection, Engine


class CS513IcTask(SqlTask):
  # column: (constraint, correction_fn)
  integrity_constraints = {}

  correct_errors=False
  recheck=False
  primary_key='id'

  def __init__(self, operation_config: dict = {}):
    super().__init__(operation_config)
    self.table = operation_config.get('table', None)
    self.correct_errors = operation_config.get('correct_errors', self.correct_errors) # by default it just reports


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
            correction_fn = None
            if isinstance(constraint, (tuple, list)):
              constraint, correction_fn = constraint

            constraint_args = [
              col,  # column name
              getattr(row, col),  # colum value
              {  # context object
                "row": row,
                "table_name": self.table,
                "connection": conn, #sqlalchemy connection
                "data": data, #pd datafram
                "primary_key_col": self.primary_key,  # usually 'id'
                "primary_key": int(row.get(self.primary_key)) # the id value
              }
            ]
            violations = constraint.check(*constraint_args)
            if violations is not None:
              all_violations[index] = violations
              violation_cols[col] = violation_cols.get(col, 0) + 1

              if self.correct_errors and correction_fn:
                # CORRECT PROBLEMS
                correction_fn(*constraint_args)

      print(f"  {len(all_violations.keys())} Rows with IC violations")

      if len(all_violations.keys()) > 0:
        cols_strs = []
        for key, count in violation_cols.items():
          cols_strs.append(f"{key} ({count})")
        print(f"  Errors were detected in the following columns: {', '.join(cols_strs)}")

      if self.correct_errors:
        print(f"  Corrections run")
    finally:
      self.connection.close()
