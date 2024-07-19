from importer2.ic.integrity_constraint import IntegrityConstraint


class IsFloat(IntegrityConstraint):
  def check(self, column, value, ctx):
    return None if isinstance(value, (int, float)) else f"{column} is not an integer"
