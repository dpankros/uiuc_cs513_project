from importer2.cs513_task import DishImportTask, MenuImportTask, MenuItemImportTask, MenuPageImportTask
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
      'source_filename': '../../../../data/Dish_sm.csv',
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
      'source_filename': '../../../../data/MenuItem_sm.csv',
      'dest_filename': '../../../../MenuItem_conv.csv',
      'sql_table': 'menu_item',
      'sql_if_exists': 'replace'
    }),
    MenuPageImportTask({
      **base_config,
      'source_filename': '../../../../data/MenuPage_sm.csv',
      'dest_filename': '../../../../MenuPage_conv.csv',
      'sql_table': 'menu_page',
      'sql_if_exists': 'replace'
    }),
    # keep after all the Import tasks as it deletes all the projects from openrefine
    ProjectCleanupTask(base_config),

    # I expect we will do something like this:
    # DishSqlUpdateTask({
    #   ...
    # }),
    #
    # and then probable
    # DishVerificationTask({
    #   ...
    # })
    # to do our quality checks at the end

  ]).run_all()


if __name__ == '__main__':
  main()
