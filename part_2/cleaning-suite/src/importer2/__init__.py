import click
from importer2.tasks import BaseConfig, get_importer_tasks, get_report_tasks, get_verification_tasks
from sqlalchemy import create_engine

from importer2.cs513_task import (
    DishImportTask, MenuImportTask, MenuItemImportTask, MenuPageImportTask,
    CreateDishViewSqlTask, CreateMenuViewSqlTask, MenuItemIcTask, MenuPageIcTask
)
from importer2.task import TaskList, ProjectCleanupTask


@click.command()
@click.option(
    "--run-imports",
    default=False,
    help="Whether to re-import data to SQLite",
)
@click.option(
    "--run-verifications",
    default=False,
    help="Whether to run verification on cleaned data",
)
@click.option(
    "--run-reports",
    default=False,
    help="Whether to run data reports"
)
@click.option(
    "--run-exports",
    default=False,
    help="Whether to export final, cleaned data to new CSV files. Files will be named '[Dish | Menu | MenuItem | MenuPage].export.csv'"
)
def main(
    run_imports: bool,
    run_verifications: bool,
    run_reports: bool,
    run_exports: bool
):
    base_config = BaseConfig(
        server_url="http://localhost:3333",
        sql_engine=create_engine('sqlite:///../../export.db'),
        max_count=10,
    )

    print(f"running imports: {run_imports}")
    print(f"running verifications: {run_verifications}")
    print(f"running reports: {run_reports}")
    print(f"running exports (TODO): {run_exports}")
    imports = get_importer_tasks(base_config, run_imports)
    verifications = get_verification_tasks(base_config, run_verifications)
    reports = get_report_tasks(base_config, run_reports)

    TaskList([
        *imports,
        # Cleaned imports - These read the CSV and clean the data prior to import
        DishImportTask({
            **base_config.as_dict(),
            'source_filename': '../../data/Dish.csv',
            'dest_filename': '../../Dish_conv.csv',
            'sql_table': 'dish',
            'sql_if_exists': 'replace'
        }),
        MenuImportTask({
            **base_config.as_dict(),
            'source_filename': '../../data/Menu.csv',
            'dest_filename': '../../Menu_conv.csv',
            'sql_table': 'menu',
            'sql_if_exists': 'replace'
        }),
        MenuItemImportTask({
            **base_config.as_dict(),
            'source_filename': '../../data/MenuItem.csv',
            'dest_filename': '../../MenuItem_conv.csv',
            'sql_table': 'menu_item',
            'sql_if_exists': 'replace'
        }),
        MenuPageImportTask({
            **base_config.as_dict(),
            'source_filename': '../../data/MenuPage.csv',
            'dest_filename': '../../MenuPage_conv.csv',
            'sql_table': 'menu_page',
            'sql_if_exists': 'replace'
        }),
        # keep after all the Import tasks as it deletes all the projects from openrefine
        ProjectCleanupTask(base_config.as_dict()),

        # SQL modification - these create SQL views and modify data in SQL
        CreateDishViewSqlTask({
            **base_config.as_dict(),
            'view_name': '_dish'
        }),
        CreateMenuViewSqlTask({
            **base_config.as_dict(),
            'view_name': '_menu'
        }),

        MenuItemIcTask({
            **base_config.as_dict(),
            'table': 'menu_item',
            'correct_errors': True,
            'name': 'MenuItem Initial Stats',
        }),
        MenuPageIcTask({
            **base_config.as_dict(),
            'table': 'menu_page',
            'correct_errors': True,
            'name': 'MenuPage Initial Stats',
        }),

        # IC Reporting
        MenuItemIcTask({
            **base_config.as_dict(),
            'table': 'menu_item',
            'correct_errors': False,
            'name': 'MenuItem Cleaned Stats',
        }),
        MenuPageIcTask({
            **base_config.as_dict(),
            'table': 'menu_page',
            'correct_errors': False,
            'name': 'MenuPage Cleaned Stats',
        }),

        *verifications,
        *reports,
    ]).run()



if __name__ == '__main__':
    main()
