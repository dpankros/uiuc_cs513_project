from importer2.ic.integrity_constraint import IntegrityConstraint
from sqlalchemy import text

class IsValidForeignKey(IntegrityConstraint):
  def __init__(self, foreign_table, column='id', allow_null=True):
    super().__init__()
    if not foreign_table:
      raise f"Invalid foreign table."
    self.foreign_table = foreign_table
    self.column = column
    self.allow_null = allow_null
    self._cache = None

  def check(self, column, value, ctx):
    if self.allow_null and value is None:  # allow null foreign keys
      return None
    value = int(value)
    if not self._cache:
      conn = ctx.get('connection', None)
      if not conn:
        raise Exception('No connection')
      self._cache = {v[0] for v in
                     conn.execute(text(f"select distinct {self.column} from {self.foreign_table}")).fetchall()}

    return None if value in self._cache else f"Foreign key {value} does not exist in table {self.foreign_table}"
