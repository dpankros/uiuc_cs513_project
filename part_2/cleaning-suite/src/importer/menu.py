import sqlite3
from importer.csv import read_csv
from checker.models.menu import create_menu_factory, create_menu_table, insert_menu

def import_menus(filename: str, conn: sqlite3.Connection) -> int:
    row_factory = create_menu_factory(strict=False)
    entries = read_csv(filename, row_factory=row_factory)        
    print("creating table for menus")
    create_menu_table(conn)
    print(f"creating {len(entries)} menus in the DB")
    for entry in entries:
        insert_menu(conn, entry)
    return len(entries)
