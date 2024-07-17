from enum import Enum
class OnErrorTypes(Enum):
    KEEP_ORIGINAL = "keep-original"
    STORE_ERROR = "store-error"
    SET_TO_BLANK = "set-to-blank"

class BaseOperation:
    def __init__(self, base_column_name=None, description=None, on_error: OnErrorTypes = OnErrorTypes.SET_TO_BLANK):
        self.base_column_name = base_column_name
        self.description = description
        self.on_error = on_error

    def value(self) -> dict:
        return {
            # "op": ?????,
            "engineConfig": {
                "facets": [],
                "mode": "row-based"
            },
            "baseColumnName": self.base_column_name,
            "onError": self.on_error.value,
            "description": self.description
        }

