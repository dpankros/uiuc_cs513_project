import aiosqlite
from importer.do_import import do_import
from checker.models.dish import create_dish_table, dish_factory, insert_dish

async def import_dishes(filename: str, conn: aiosqlite.Connection) -> int:
    return await do_import(
        filename,
        conn=conn,
        row_factory=dish_factory,
        table_creator=create_dish_table,
        inserter=insert_dish
    )
