import sqlite3
from typing import Callable

type Check = tuple[str, Callable[[sqlite3.Connection], str]]
