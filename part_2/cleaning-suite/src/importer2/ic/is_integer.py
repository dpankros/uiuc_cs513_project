from importer2.ic.integrity_constraint import IntegrityConstraint


class IsInteger(IntegrityConstraint):
  def check(self, column, value, ctx):
    return None if value.is_integer() else f"{column} is not an integer"
