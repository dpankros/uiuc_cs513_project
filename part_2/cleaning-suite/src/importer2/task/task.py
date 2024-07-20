from importer2.openrefine.config import Config

class BaseTask:
  name = "BaseTask"

  def __init__(self, operation_config: dict = {}):
    self.config = Config(operation_config)
    if 'name' in operation_config:
      self.name = operation_config.get('name')

  def run(self):
    raise NotImplementedError()
