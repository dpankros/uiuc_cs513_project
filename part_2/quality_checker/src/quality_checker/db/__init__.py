from typing import Callable
import sqlite3


type RowFactory[T] = Callable[[sqlite3.Cursor, sqlite3.Row], T]


def run_query[T](
    conn: sqlite3.Connection,
    *,
    query: str,
    row_factory: RowFactory[T],
) -> list[T]:
    conn.row_factory = row_factory
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()
