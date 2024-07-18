from openrefine import Server

from .task import BaseTask


# TODO: this is largely just a placeholder.  I took a stab at a basline task for sql operations but feel free to change
class SqlTask(BaseTask):
  def __init__(self, operation_config: dict = {}):
    super().__init__(operation_config)
    self.server_url = operation_config['server_url']

    self.sql_engine = operation_config['sql_engine'] if 'sql_engine' in operation_config else None
    self.sql_table = operation_config['sql_table'] if 'sql_table' in operation_config else None


  def run(self):
    self.server = Server(self.server_url) if self.server_url else Server()
    #self.connection = CREATE THE SERVER CONNECTION FOR SQL

    return self
