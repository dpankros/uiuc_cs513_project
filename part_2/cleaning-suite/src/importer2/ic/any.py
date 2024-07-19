from importer2.ic.integrity_constraint import IntegrityConstraint

class Any(IntegrityConstraint):
  """
  Logical OR - Success of any is success of the whole proposition
  """

  def __init__(self, *constraints):
    super().__init__()
    self.constraints = constraints

  def check(self, column, value, ctx):
    r_accum = []
    for c in self.constraints:
      r = c.check(column, value, ctx)
      if r is None or len(r) == 0:
        return None
      else:
        r_accum = [*r_accum, r]

    return r_accum
