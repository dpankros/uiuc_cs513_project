from typing import Any, Callable
import sqlite3


type RowFactory[T] = Callable[[dict[str | Any, Any]], T]


def run_query[T](
    conn: sqlite3.Connection,
    *,
    query: str,
    row_factory: RowFactory[T],
) -> list[T]:
    def factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> T:
        row_dict = {
            column: value
            for column, value in zip([column[0] for column in cursor.description], row)
        }
        return row_factory(row_dict)

    conn.row_factory = factory
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()
