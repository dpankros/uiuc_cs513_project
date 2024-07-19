from importer2.ic.integrity_constraint import IntegrityConstraint


class IsDefined(IntegrityConstraint):
  def check(self, column, value, ctx):
    return None if value is not None and not math.isnan(value) else f"{column} is not defined"
