from sqlalchemy import text

from .cs513_sql_task import CS513SqlTask


class DishSqlTask(CS513SqlTask):
  name = "Create Dish View"

  def run(self):
    super().run()

    view_name = self.config.view_name
    # Tasks:
    # [ ] calculate menus_appeared
    # [ ] calculate times_appeared
    # [ ] caclulate first_appeared
    # [ ] calculate last_appeared
    # [ ] caclulate lowest_price
    # [ ] calculate highest_price

    # TODO: when there are zeros in mi.price the min calculation is thrown off (lowest price)
    #  highest_price is off in some instances too

    view_select = """    
select
    d.id as id,
    d.norm_name as name,
    d.description as description,
    count(m.id) as menus_appeared,
    count(mp.id) as times_appeared,
    min(CAST(substr(date, 0, 5) as INTEGER)) as first_appeared,
    max(CAST(substr(date, 0, 5) as INTEGER)) as last_appeared,
    min(mi.price) as lowest_price, 
    max(mi.price) as highest_price
from dish d
left join menu_item mi on d.id = mi.dish_id
left join main.menu_page mp on mi.menu_page_id = mp.id
left join main.menu m on mp.menu_id = m.id
group by d.id
order by d.id asc
    """
    try:
      txn = self.connection.begin()
      self.connection.execute(text(f"DROP VIEW IF EXISTS {view_name};"))
      self.connection.execute(text(f"CREATE VIEW {view_name} AS {view_select};"))
      txn.commit()
    finally:
      self.connection.close()
