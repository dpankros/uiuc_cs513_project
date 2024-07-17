from openrefine import Server, Project
from operation import OperationList
from dish_import_operation import DishImportOperation
from menu_import_operation import MenuImportOperation
from project_cleanup_operation import ProjectCleanupOperation
from sqlalchemy import create_engine

if __name__ == '__main__':
    base_config = {
        'server_url': "http://localhost:3333",
        'sql_engine': create_engine('sqlite:///../../../../export.db')
    }

    OperationList([
        # DishImportOperation({
        #     **base_config,
        #     'source_filename': '../../../../data/Dish.csv',
        #     'dest_filename': '../../../../Dish_conv.csv',
        #     'sql_table': 'dish',
        #     'sql_if_exists': 'replace'
        # }),
        MenuImportOperation({
            **base_config,
            'source_filename': '../../../../data/Menu.csv',
            'dest_filename': '../../../../Menu_conv.csv',
            'sql_table': 'menu',
            'sql_if_exists': 'replace'
        }),

        # keep this last as it deletes all the projects from openrefine
        ProjectCleanupOperation(base_config)
    ]).run_all()

