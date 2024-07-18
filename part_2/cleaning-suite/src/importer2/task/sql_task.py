from sqlalchemy.engine import Engine, Connection

from .task import BaseTask


# TODO: this is largely just a placeholder.  I took a stab at a basline task for sql operations but feel free to change
class SqlTask(BaseTask):
  def __init__(self, operation_config: dict = {}):
    super().__init__(operation_config)
    self.sql_engine: Engine = operation_config['sql_engine'] if 'sql_engine' in operation_config else None
    self.sql_table: str = operation_config['sql_table'] if 'sql_table' in operation_config else None

  def run(self):
    self.connection: Connection = self.sql_engine.connect()
    return self
