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


    def run(self):
        self.server = Server(self.server_url) if self.server_url else Server()

        return self


