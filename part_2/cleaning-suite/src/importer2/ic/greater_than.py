from importer2.ic.integrity_constraint import IntegrityConstraint


class GreaterThan(IntegrityConstraint):
  def __init__(self, value):
    self.threshold = value

  def check(self, column, value, ctx):
    return None if value > self.threshold else f"{column} is not greater than {self.threshold} ({value})"
