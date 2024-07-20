from sqlalchemy import text

from .cs513_sql_task import CS513SqlTask


class CreateDishViewSqlTask(CS513SqlTask):
  name = "Create Dish View"

  def run(self):
    super().run()

    view_name = self.config.view_name
    # Tasks:
    # [x] calculate menus_appeared
    # [x] calculate times_appeared
    # [x] caclulate first_appeared
    # [x] calculate last_appeared
    # [x] caclulate lowest_price
    # [x] calculate highest_price

    # TODO: when there are zeros in mi.price the min calculation is thrown off (lowest price)
    #  highest_price is off in some instances too

    view_select = """    
select
    id as id,
    name as name,
    description as description,
    max(menus_appeared, 1) as menus_appeared,
    max(times_appeared, 1) as times_appeared,
    max(1852, first_appeared) as first_appeared,
    min(last_appeared, 2024) as last_appeared,
    lowest_price as lowest_price,
    highest_price as highest_price
from (select d.id                                     as id,
             d.norm_name                              as name,
             d.description                            as description,
             max(count(m.id), 1)                      as menus_appeared,
             max(count(mp.id), 1)                     as times_appeared,
             min(CAST(substr(date, 0, 5) as INTEGER)) as first_appeared,
             max(CAST(substr(date, 0, 5) as INTEGER)) as last_appeared,
             min(mi.price)                            as lowest_price,
             max(mi.price)                            as highest_price
      from dish d
               left join menu_item mi on d.id = mi.dish_id
               left join main.menu_page mp on mi.menu_page_id = mp.id
               left join main.menu m on mp.menu_id = m.id
      group by d.id
      order by d.id asc)

    """
    try:
      txn = self.connection.begin()
      with txn.connection as conn:
        conn.execute(text(f"DROP VIEW IF EXISTS {view_name};"))
        conn.execute(text(f"CREATE VIEW {view_name} AS {view_select};"))
        txn.commit()
    finally:
      self.connection.close()
