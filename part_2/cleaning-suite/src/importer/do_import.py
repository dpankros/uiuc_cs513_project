import aiosqlite
import asyncio
from typing import Awaitable, Callable
from checker.db import RowFactory
from importer.csv import read_csv


async def do_import[T](
    filename: str,
    *,
    conn: aiosqlite.Connection,
    row_factory: RowFactory[T],
    table_creator: Callable[[aiosqlite.Connection], Awaitable[None]],
    inserter: Callable[[aiosqlite.Connection, T], Awaitable[None]],
) -> int:
    entries = read_csv(filename, row_factory=row_factory)
    print("creating table")
    await table_creator(conn)
    print(f"creating {len(entries)} entries in the DB")
    coros: list[Awaitable[None]] = [inserter(conn, entry) for entry in entries]
    await asyncio.gather(*coros)
    return len(entries)
