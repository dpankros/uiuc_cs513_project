from openrefine import Server


class BaseOperation:
    def __init__(self, operation_config: dict = {}):
        self.config = operation_config

    def run(self):
        raise NotImplementedError()


class OperationList(list):
    def run_all(self):
        for op in self:
            op.run()


class OpenRefineOperation(BaseOperation):
    def __init__(self, operation_config: dict = {}):
        super().__init__(operation_config)
        self.server_url = operation_config['server_url']

        self.source_filename = operation_config['source_filename'] if 'source_filename' in operation_config else None
        self.dest_filename = operation_config['dest_filename'] if 'dest_filename' in operation_config else None
        self.server_url = operation_config['server_url'] if 'server_url' in operation_config else None
        self.sql_engine = operation_config['sql_engine'] if 'sql_engine' in operation_config else None
        self.sql_table = operation_config['sql_table'] if 'sql_table' in operation_config else None
        self.sql_if_exists = operation_config['sql_if_exists'] if 'sql_if_exists' in operation_config else None

    def run(self):
        self.server = Server(self.server_url) if self.server_url else Server()

        return self

    def export(self, project):
        """
        Exports to a location based on the config
        :param project:
        :return:
        """
        if self.sql_engine:
            project.to_sql(self.sql_engine, self.sql_table, if_exists=self.sql_if_exists)

        if self.dest_filename:
            project.export_rows_to_file(self.dest_filename)
