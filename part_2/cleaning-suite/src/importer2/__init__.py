from importer2.cs513_task import DishImportTask, MenuImportTask, MenuItemImportTask, MenuPageImportTask, CreateDishViewSqlTask, CreateMenuViewSqlTask
from importer2.openrefine import Server, Project
from importer2.task import TaskList, ProjectCleanupTask
from sqlalchemy import create_engine


def main():
  base_config = {
    'server_url': "http://localhost:3333",
    'sql_engine': create_engine('sqlite:///../../../../export.db')
  }

  TaskList([
    DishImportTask({
      **base_config,
      'source_filename': '../../../../data/Dish.csv',
      'dest_filename': '../../../../Dish_conv.csv',
      'sql_table': 'dish',
      'sql_if_exists': 'replace'
    }),
    MenuImportTask({
      **base_config,
      'source_filename': '../../../../data/Menu.csv',
      'dest_filename': '../../../../Menu_conv.csv',
      'sql_table': 'menu',
      'sql_if_exists': 'replace'
    }),
    MenuItemImportTask({
      **base_config,
      'source_filename': '../../../../data/MenuItem.csv',
      'dest_filename': '../../../../MenuItem_conv.csv',
      'sql_table': 'menu_item',
      'sql_if_exists': 'replace'
    }),
    MenuPageImportTask({
      **base_config,
      'source_filename': '../../../../data/MenuPage.csv',
      'dest_filename': '../../../../MenuPage_conv.csv',
      'sql_table': 'menu_page',
      'sql_if_exists': 'replace'
    }),
    # keep after all the Import tasks as it deletes all the projects from openrefine
    # ProjectCleanupTask(base_config),

    CreateDishViewSqlTask({
      **base_config,
      'view_name': '_dish'
    }),
    CreateMenuViewSqlTask({
      **base_config,
      'view_name': '_menu'
    }),
    #
    # and then probable
    # DishVerificationTask({
    #   ...
    # })
    # to do our quality checks at the end

  ]).run()


if __name__ == '__main__':
  main()
