from .base_operation import BaseOperation


class ColumnAdditionOp(BaseOperation):

    def __init__(self, base_column_name: str = None, new_column_name: str = None, expression: str = None,
                 column_insert_index: int = None, **kwargs) -> dict:
        super().__init__(
            base_column_name=base_column_name,
            description=f"Create column {new_column_name} from grel modification of {base_column_name}",
            **kwargs)
        self.new_column_name = new_column_name
        self.column_insert_index = column_insert_index
        self.expression = expression

    def value(self) -> dict:
        return {
            **super().value(),
            "op": "core/column-addition",
            "expression": f"grel:{self.expression}",
            "newColumnName": self.new_column_name,
            "columnInsertIndex": self.column_insert_index
        }
