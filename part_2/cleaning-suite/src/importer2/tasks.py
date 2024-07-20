from dataclasses import dataclass
from typing import Sequence
from importer2.cs513_task.dish_verification_task import DishVerificationTask
from importer2.cs513_task.menu_item_report_task import MenuItemReportTask
from importer2.cs513_task.menu_item_verification_task import MenuItemVerificationTask
from importer2.cs513_task.menu_page_report_task import MenuPageReportTask
from importer2.cs513_task.menu_page_verification_task import MenuPageVerificationTask
from importer2.cs513_task.menu_verification_task import MenuVerificationTask
from importer2.cs513_task.verbatim_import_task import VerbatimImportTask
from importer2.task.task import BaseTask
from sqlalchemy import Engine


@dataclass
class BaseConfig:
    server_url: str
    sql_engine: Engine
    max_count: int

    def as_dict(self) -> dict[str, str | Engine | int]:
        return {
            "server_url": self.server_url,
            "sql_engine": self.sql_engine,
            "max_count": self.max_count,
        }

def get_verification_tasks(
    base_config: BaseConfig,
    run_verifications: bool
) -> Sequence[BaseTask]:
    """
    if run_verifications==True, get a list of tasks that verify data on the 
    "cleaned" data in appropriate SQLite tables. Otherwise, return an empty
    list

    These judge whether the data is an exact match so it's not very good
    """
    return [
        DishVerificationTask(base_config.as_dict()),
        MenuVerificationTask(base_config.as_dict()),
        MenuPageVerificationTask(base_config.as_dict()),
        MenuItemVerificationTask(base_config.as_dict()),
    ] if run_verifications else []

def get_importer_tasks(
    base_config: BaseConfig,
    run_imports: bool
) -> Sequence[BaseTask]:
    """
    if run_imports==True, get a list of tasks that import raw CSV data from 
    Dish.csv, Menu.csv, MenuItem.csv, and MenuPage.csv into "orig" tables in 
    SQLite. Otherwise, return an empty list
    """
    # Verbatim imports - Make a copy of the data in sqlite without ANY modification
    return [
        VerbatimImportTask({
            **base_config.as_dict(),
            'source_filename': '../../data/Dish.csv',
            'sql_table': 'dish_orig',
            'sql_if_exists': 'replace',
            'name': 'Import dish_orig unmodified data',
        }),
        VerbatimImportTask({
            **base_config.as_dict(),
            'source_filename': '../../data/Menu.csv',
            'sql_table': 'menu_orig',
            'sql_if_exists': 'replace',
            'name': 'Import menu_orig unmodified data',
        }),
        VerbatimImportTask({
            **base_config.as_dict(),
            'source_filename': '../../data/MenuItem.csv',
            'sql_table': 'menu_item_orig',
            'sql_if_exists': 'replace',
            'name': 'Import menu_item_orig unmodified data',
        }),
        VerbatimImportTask({
            **base_config.as_dict(),
            'source_filename': '../../data/MenuPage.csv',
            'sql_table': 'menu_page_orig',
            'sql_if_exists': 'replace',
            'name': 'Import menu_page_orig unmodified data',
        }),
    ] if run_imports else []

def get_report_tasks(base_config: BaseConfig, run_reports: bool) -> Sequence[BaseTask]:
    """
    If run_reports==True, get a list of Tasks that report on data in the tables
    with "clean" data in SQLite. Otherwise, return an empty list
    """
    # TODO: These should show the range of
    return [
        MenuItemReportTask({**base_config.as_dict(), 'table': 'menu_item_orig', 'name': 'Original Menu Item IC Violations Task'}),
        MenuItemReportTask({**base_config.as_dict(), 'table': 'menu_item', 'name': 'Updated Menu Item IC Violations Task'}),
        MenuPageReportTask({**base_config.as_dict(), 'table': 'menu_page_orig', 'name': 'Original Menu Page IC Violations Task'}),
        MenuPageReportTask({**base_config.as_dict(), 'table': 'menu_page', 'name': 'Update Menu Item IC Violations Task'}),
    ] if run_reports else []
