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

    # @staticmethod
    # def op(orig_column: str, grel_exp: str = None, operation: str=None, new_column: str = None, index: int = None) -> {}:
    #     op = None
    #     expression = None
    #     onError = None
    #     description = None
    #
    #     if operation is None:
    #         if orig_column is not None and new_column is not None and grel_exp is not None:
    #             op = "core/column-addition"
    #             grel_exp = f'grel:{grep_exp}'
    #             description = f"Create column {new_column} from grel modification of {orig_column}"
    #
    #         if new_column is not None and new_column is None and grel_exp is not None:
    #             op = "core/text-transform"
    #             description = f"Update column {new_column} with grel modification"
    #
    #         if new_column is not None and new_column is None and grel_exp is not None:
    #             op = "core/column-rename"
    #             description = f"Rename column {new_column} to {new_column}"
    #
    # op = {
    #         "op": op,
    #         "engineConfig": {
    #             "facets": [],
    #             "mode": "row-based"
    #         },
    #         "baseColumnName": orig_column,
    #         # "expression": f'grel:{grep_exp}',
    #         "onError": "set-to-blank",
    #         # "newColumnName": new_column,
    #         # "columnInsertIndex": index,
    #         "description": description
    #     }
    #
    # if expression is not None:
    #     op['expression'] = grel_exp
    # if newColumnName is not None:
    #     op['newColumnName'] = new_column
    # if index is not None:
    #     op['columnInsertIndex'] = index
    #
    # return op
    #
    # @staticmethod
    # def new_column_op(orig_column: str, grel_exp: str, operation=None, new_column: str = None, index: int = None) -> [
    #     {}]:
    #     return OpenRefineOperation.op(orig_column, grel_exp, operation="core/column-addition", new_column=new_column,
    #                                   index=index)
