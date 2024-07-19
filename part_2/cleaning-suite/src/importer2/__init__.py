from sqlalchemy import create_engine

from importer2.cs513_task import DishImportTask, MenuImportTask, MenuItemImportTask, MenuPageImportTask, \
  CreateDishViewSqlTask, CreateMenuViewSqlTask, DishVerificationTask, MenuVerificationTask, MenuPageVerificationTask, \
  MenuItemVerificationTask, VerbatimImportTask
from importer2.openrefine import Server, Project
from importer2.task import TaskList, ProjectCleanupTask


def main():
  base_config = {
    'server_url': "http://localhost:3333",
    'sql_engine': create_engine('sqlite:///../../../../export.db'),
    "max_count": 10,
  }

  TaskList([
    #
    # Verbatim imports - Make a copy of the data in sqlite without ANY modification
    #

    # VerbatimImportTask({
    #   **base_config,
    #   'source_filename': '../../../../data/Dish.csv',
    #   'sql_table': 'dish_orig',
    #   'sql_if_exists': 'replace'
    # }),
    # VerbatimImportTask({
    #   **base_config,
    #   'source_filename': '../../../../data/Menu.csv',
    #   'sql_table': 'menu_orig',
    #   'sql_if_exists': 'replace'
    # }),
    # VerbatimImportTask({
    #   **base_config,
    #   'source_filename': '../../../../data/MenuItem.csv',
    #   'sql_table': 'menu_item_orig',
    #   'sql_if_exists': 'replace'
    # }),
    # VerbatimImportTask({
    #   **base_config,
    #   'source_filename': '../../../../data/MenuPage.csv',
    #   'sql_table': 'menu_page_orig',
    #   'sql_if_exists': 'replace'
    # }),

    #
    # Cleaned imports - These read the CSV and clean the data prior to import
    #

    # DishImportTask({
    #   **base_config,
    #   'source_filename': '../../../../data/Dish.csv',
    #   'dest_filename': '../../../../Dish_conv.csv',
    #   'sql_table': 'dish',
    #   'sql_if_exists': 'replace'
    # }),
    # MenuImportTask({
    #   **base_config,
    #   'source_filename': '../../../../data/Menu.csv',
    #   'dest_filename': '../../../../Menu_conv.csv',
    #   'sql_table': 'menu',
    #   'sql_if_exists': 'replace'
    # }),
    # MenuItemImportTask({
    #   **base_config,
    #   'source_filename': '../../../../data/MenuItem.csv',
    #   'dest_filename': '../../../../MenuItem_conv.csv',
    #   'sql_table': 'menu_item',
    #   'sql_if_exists': 'replace'
    # }),
    # MenuPageImportTask({
    #   **base_config,
    #   'source_filename': '../../../../data/MenuPage.csv',
    #   'dest_filename': '../../../../MenuPage_conv.csv',
    #   'sql_table': 'menu_page',
    #   'sql_if_exists': 'replace'
    # }),
    # keep after all the Import tasks as it deletes all the projects from openrefine
    # ProjectCleanupTask(base_config),

    #
    # SQL modification - these create SQL views and modify data in SQL
    #

    # CreateDishViewSqlTask({
    #   **base_config,
    #   'view_name': '_dish'
    # }),
    # CreateMenuViewSqlTask({
    #   **base_config,
    #   'view_name': '_menu'
    # }),

    #
    # Verification tasks - these judge whether the data is "correct"
    #
    DishVerificationTask(base_config),
    MenuVerificationTask(base_config),
    MenuPageVerificationTask(base_config),
    MenuItemVerificationTask(base_config),


  ]).run()


if __name__ == '__main__':
  main()
