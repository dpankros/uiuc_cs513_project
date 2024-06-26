--- Table Counts
select 'MenuItem', count(*) from MenuItem MI
union
select 'Dish', count(*) from Dish D
union
select 'Menu', count(*) from Menu M
union
select 'MenuPage', count(*) from MenuPage MP;


--- Count of uuids in MenuPage
select distinct uuid from MenuPage order by uuid asc;

--- Domain of xpos and ypos in MenuItem

select min(xpos), max(xpos), min(ypos), max(ypos) from MenuItem;

--- MenuItems and their missing Pages
select * from MenuItem MI
                  left outer join main.MenuPage MP on MI.menu_page_id = MP.id
where MP.id is null;

--- MenuItems and their missing Dishes
select * from MenuItem MI
                  left outer join main.Dish D on MI.dish_id = D.id
where D.id is null;

--- MenuPages and their missing Menus
select * from MenuPage MP
                  left outer join main.Menu M on M.id = MP.menu_id
where M.id is NULL;

--- Menus having page_counts that differ from a count of MenuPage rows
select M.id, count(MP.id), M.page_count from Menu M
                                                 left join main.MenuPage MP on M.id = MP.menu_id
group by M.id having count(MP.id) <> M.page_count;

--- Menus having dish_counts that differ from the number of dishes appearing in MenuPages
select M.id, MP.page_number, M.page_count, count(D.id) as 'Dishes in DB', M.dish_count from Menu M
                                                                                                left join main.MenuPage MP on M.id = MP.menu_id
                                                                                                left join main.MenuItem MI on MP.id = MI.menu_page_id
                                                                                                left join main.Dish D on MI.dish_id = D.id
group by M.id having count(D.id) <> M.dish_count
order by M.id asc, MP.page_number asc;
