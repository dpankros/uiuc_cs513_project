from importer2.ic.integrity_constraint import IntegrityConstraint


class Unique(IntegrityConstraint):
  def check(self, column, value, ctx):
    # only evaluate ONCE
    if hasattr(self, 'result'):
      return self.result

    data = ctx['data']
    self.result = None if data[column].is_unique else f"Not unique"
    return self.result
