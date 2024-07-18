from sqlalchemy import text

from .cs513_sql_task import CS513SqlTask


class CreateMenuViewSqlTask(CS513SqlTask):
  name = "Create Menu View"

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
    m.id,
    m.norm_name as name,
    m.norm_sponsor as sponsor,
    m.norm_event as event,
    m.norm_venue as venue,
    m.norm_place as place,
    m.norm_physical_description as physical_description,
    m.norm_occasion as occasion,
    m.norm_notes as notes,
    m.call_number as call_number,
    m.date as date,
    m.norm_location as location,
    m.currency as currency,
    m.currency_symbol as currency_symbol,
    m.status as status,
    count(mp.id) as page_count, 
    count(mi.dish_id) as dish_count 
from menu m
left join main.menu_page mp on m.id = mp.menu_id
left join main.menu_item mi on mp.id = mi.menu_page_id
group by m.id
    """
    try:
      txn = self.connection.begin()
      self.connection.execute(text(f"DROP VIEW IF EXISTS {view_name};"))
      self.connection.execute(text(f"CREATE VIEW {view_name} AS {view_select};"))
      txn.commit()
    finally:
      self.connection.close()
