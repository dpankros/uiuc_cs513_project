import aiosqlite
from dataclasses import fields, dataclass


@dataclass
class Model:
    pass


async def insert_entry(
    table_name: str, conn: aiosqlite.Connection, entry: Model
) -> None:
    columns = [field.name for field in fields(entry)]
    values = [getattr(entry, field) for field in columns]

    # Create the INSERT statement
    sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in columns])})"

    # Execute the statement
    await conn.execute(sql, values)
    await conn.commit()
