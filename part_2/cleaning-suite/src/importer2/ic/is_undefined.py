import math

from importer2.ic.integrity_constraint import IntegrityConstraint


class IsUndefined(IntegrityConstraint):
  def check(self, column, value, ctx):
    # undefined can either be None or NaN
    return None if value is None or math.isnan(value) else f"{column} is defined"
