class BaseTask:
  def __init__(self, operation_config: dict = {}):
    self.config = operation_config

  def run(self):
    raise NotImplementedError()
