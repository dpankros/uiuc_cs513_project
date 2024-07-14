import aiosqlite
from importer.do_import import do_import
from checker.models.menu import create_menu_factory, create_menu_table, insert_menu

async def import_menus(filename: str, conn: aiosqlite.Connection) -> int:
    return await do_import(
        filename,
        conn=conn,
        row_factory=create_menu_factory(strict=False),
        table_creator=create_menu_table,
        inserter=insert_menu,
    )
