from importer2.cs513_operations import DishImportOperation, MenuImportOperation, MenuItemImportOperation
from importer2.openrefine import Server, Project
from importer2.operation_list import OperationList
from importer2.project_cleanup_operation import ProjectCleanupOperation
from sqlalchemy import create_engine


def main():
  base_config = {
    'server_url': "http://localhost:3333",
    'sql_engine': create_engine('sqlite:///../../../../export.db')
  }

  OperationList([
    DishImportOperation({
        **base_config,
        'source_filename': '../../../../data/Dish.csv',
        'dest_filename': '../../../../Dish_conv.csv',
        'sql_table': 'dish',
        'sql_if_exists': 'replace'
    }),
    MenuImportOperation({
      **base_config,
      'source_filename': '../../../../data/Menu.csv',
      'dest_filename': '../../../../Menu_conv.csv',
      'sql_table': 'menu',
      'sql_if_exists': 'replace'
    }),
    MenuItemImportOperation({
      **base_config,
      'source_filename': '../../../../data/MenuItem_sm.csv',
      'dest_filename': '../../../../MenuItem_conv.csv',
      'sql_table': 'menu_item',
      'sql_if_exists': 'replace'
    }),
    # MenuPageImportOperation({
    #   **base_config,
    #   'source_filename': '../../../../data/MenuPage_sm.csv',
    #   'dest_filename': '../../../../MenuPage_conv.csv',
    #   'sql_table': 'menu',
    #   'sql_if_exists': 'replace'
    # }),

    # keep this last as it deletes all the projects from openrefine
    ProjectCleanupOperation(base_config)
  ]).run_all()


if __name__ == '__main__':
  main()
