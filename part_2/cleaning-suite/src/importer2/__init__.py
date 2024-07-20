from sqlalchemy import create_engine

from importer2.cs513_task import DishImportTask, MenuImportTask, MenuItemImportTask, MenuPageImportTask, \
    CreateDishViewSqlTask, CreateMenuViewSqlTask, DishVerificationTask, MenuVerificationTask, MenuPageVerificationTask, \
    MenuItemVerificationTask, VerbatimImportTask, MenuItemReportTask, MenuPageReportTask, MenuItemIcTask, MenuPageIcTask
from importer2.openrefine import Server, Project
from importer2.task import TaskList, ProjectCleanupTask


def main():
    base_config = {
        'server_url': "http://localhost:3333",
        'sql_engine': create_engine('sqlite:///../../export.db'),
        "max_count": 10,
    }

    TaskList([
        #
        # Verbatim imports - Make a copy of the data in sqlite without ANY modification
        #

        # VerbatimImportTask({
        #   **base_config,
        #   'source_filename': '../../data/Dish.csv',
        #   'sql_table': 'dish_orig',
        #   'sql_if_exists': 'replace',
        #   'name': 'Import dish_orig unmodified data',
        # }),
        # VerbatimImportTask({
        #   **base_config,
        #   'source_filename': '../../data/Menu.csv',
        #   'sql_table': 'menu_orig',
        #   'sql_if_exists': 'replace',
        #   'name': 'Import menu_orig unmodified data',
        # }),
        # VerbatimImportTask({
        #   **base_config,
        #   'source_filename': '../../data/MenuItem.csv',
        #   'sql_table': 'menu_item_orig',
        #   'sql_if_exists': 'replace',
        #   'name': 'Import menu_item_orig unmodified data',
        # }),
        # VerbatimImportTask({
        #   **base_config,
        #   'source_filename': '../../data/MenuPage.csv',
        #   'sql_table': 'menu_page_orig',
        #   'sql_if_exists': 'replace',
        #   'name': 'Import menu_page_orig unmodified data',
        # }),
        #
        # #
        # # Cleaned imports - These read the CSV and clean the data prior to import
        # #
        #
        DishImportTask({
          **base_config,
          'source_filename': '../../data/Dish.csv',
          'dest_filename': '../../Dish_conv.csv',
          'sql_table': 'dish',
          'sql_if_exists': 'replace'
        }),
        MenuImportTask({
          **base_config,
          'source_filename': '../../data/Menu.csv',
          'dest_filename': '../../Menu_conv.csv',
          'sql_table': 'menu',
          'sql_if_exists': 'replace'
        }),
        MenuItemImportTask({
          **base_config,
          'source_filename': '../../data/MenuItem.csv',
          'dest_filename': '../../MenuItem_conv.csv',
          'sql_table': 'menu_item',
          'sql_if_exists': 'replace'
        }),
        MenuPageImportTask({
          **base_config,
          'source_filename': '../../data/MenuPage.csv',
          'dest_filename': '../../MenuPage_conv.csv',
          'sql_table': 'menu_page',
          'sql_if_exists': 'replace'
        }),
        # # keep after all the Import tasks as it deletes all the projects from openrefine
        ProjectCleanupTask(base_config),

        #
        # SQL modification - these create SQL views and modify data in SQL
        #

        CreateDishViewSqlTask({
            **base_config,
            'view_name': '_dish'
        }),
        CreateMenuViewSqlTask({
            **base_config,
            'view_name': '_menu'
        }),

        MenuItemIcTask({
            **base_config,
            'table': 'menu_item',
            'correct_errors': True,
            'name': 'MenuItem Initial Stats',
        }),
        MenuPageIcTask({
            **base_config,
            'table': 'menu_page',
            'correct_errors': True,
            'name': 'MenuPage Initial Stats',
        }),

        #
        # IC Reporting
        #
        MenuItemIcTask({
            **base_config,
            'table': 'menu_item',
            'correct_errors': False,
            'name': 'MenuItem Cleaned Stats',
        }),
        MenuPageIcTask({
            **base_config,
            'table': 'menu_page',
            'correct_errors': False,
            'name': 'MenuPage Cleaned Stats',
        }),

        # Verification tasks - these judge whether the data is an exact match so it's not very good
        #
        # DishVerificationTask(base_config),
        # MenuVerificationTask(base_config),
        # MenuPageVerificationTask(base_config),
        # MenuItemVerificationTask(base_config),

        #
        # Reporting tasks - these provide data outputs.
        # TODO: These should show the range of
        #
        # MenuItemReportTask({**base_config, 'table': 'menu_item_orig', 'name': 'Original Menu Item IC Violations Task'}),
        # MenuItemReportTask({**base_config, 'table': 'menu_item', 'name': 'Updated Menu Item IC Violations Task'}),
        # MenuPageReportTask({**base_config, 'table': 'menu_page_orig', 'name': 'Original Menu Page IC Violations Task'}),
        # MenuPageReportTask({**base_config, 'table': 'menu_page', 'name': 'Update Menu Item IC Violations Task'}),

    ]).run()


if __name__ == '__main__':
    main()
