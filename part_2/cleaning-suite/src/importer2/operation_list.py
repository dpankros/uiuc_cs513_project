class OperationList(list):
  def run_all(self):
    for op in self:
      op.run()
