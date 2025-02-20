from enum import Enum

from importer2.openrefine.config import Config


class OnErrorTypes(Enum):
  KEEP_ORIGINAL = "keep-original"
  STORE_ERROR = "store-error"
  SET_TO_BLANK = "set-to-blank"


class BaseOperation:
  def __init__(self, **kwargs):
    self.config = Config(kwargs)

  def value(self) -> dict:
    return {}

  def to_json(self):
    return self.value

  def __getattr__(self, item):
    return self.config[item] if item in self.config else None
