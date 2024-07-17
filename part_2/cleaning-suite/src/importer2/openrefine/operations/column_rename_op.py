from .base_operation import BaseOperation


class ColumnRenameOp(BaseOperation):
    def value(self) -> dict:
        return {
            "op": "core/column-rename",
            "oldColumnName": self.old_column_name,
            "newColumnName": self.new_column_name,
            "description": f"Rename column {self.old_column_name} to {self.new_column_name}"
        }
