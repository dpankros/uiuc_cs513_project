from .base_operation import BaseOperation


class ColumnRemovalOp(BaseOperation):
    def value(self) -> dict:
        return {
            "columnName": self.column_name,
            "op": "core/column-removal",
            "description": f"Remove column {self.column_name}"
        }
