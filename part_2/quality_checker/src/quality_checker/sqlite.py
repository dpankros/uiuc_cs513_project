import sqlite3


def get_table_counts(db_path: str) -> list[tuple[str, int]]:
    query = """
    select 'MenuItem', count(*) from MenuItem MI
    union
    select 'Dish', count(*) from Dish D
    union
    select 'Menu', count(*) from Menu M
    union
    select 'MenuPage', count(*) from MenuPage MP;
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    lst: list[tuple[str, int]] = []
    for row in results:
        lst.append(row)
    return lst
