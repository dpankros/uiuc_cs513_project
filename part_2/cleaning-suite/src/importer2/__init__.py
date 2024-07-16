from openrefine import Server, Project
from operation import OperationList
from dish_import_operation import DishImportOperation
from project_cleanup_operation import ProjectCleanupOperation

if __name__ == '__main__':
    base_config = {
        'server_url': "http://localhost:3333"
    }

    OperationList([
        DishImportOperation({
            **base_config,
            'source_filename': '../../../../data/Dish_sm.csv',
            'dest_filename': '../../../../Dish_conv.csv'
        }),

        # keep this last as it deletes all the projects from openrefine
        ProjectCleanupOperation(base_config)
    ]).run_all()

