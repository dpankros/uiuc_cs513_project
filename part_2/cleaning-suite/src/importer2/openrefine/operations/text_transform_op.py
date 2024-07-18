from .base_operation import BaseOperation, OnErrorTypes


class TextTransformOp(BaseOperation):
  # def __init__(self, **kwargs) -> dict:
  #     super().__init__(**kwargs)
  #     self.config['on_error'] = self.config['on_error'] if 'on_error' in self.config else OnErrorTypes.SET_TO_BLANK

  def value(self) -> dict:
    return {
      "op": "core/text-transform",
      "engineConfig": {
        "facets": [],
        "mode": "row-based"
      },
      "columnName": self.column_name,
      "expression": f"grel:{self.expression}",
      "onError": (self.on_error or OnErrorTypes.SET_TO_BLANK).value,
      "repeat": self.repeat or False,
      "repeatCount": self.repeat_count or 10,
      "description": f"Text transform on cells in column {self.column_name} using expression grel:{self.expression}"
    }

    # return {
    #     "op": "core/column-addition",
    #     "engineConfig": {
    #         "facets": [],
    #         "mode": "row-based"
    #     },
    #     "baseColumnName": self.base_column_name,
    #     "onError": self.on_error.value,
    #     "expression": f"grel:{self.expression}",
    #     "newColumnName": self.new_column_name,
    #     "columnInsertIndex": self.column_insert_index,
    #     "description": f"Create column {self.new_column_name} from grel modification of {self.base_column_name}"
    # }
