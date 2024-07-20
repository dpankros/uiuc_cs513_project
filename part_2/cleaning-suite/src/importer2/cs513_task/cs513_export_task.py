import pandas as pd
from typing import Any, Self
from importer2.cs513_task.cs513_sql_task import CS513SqlTask

class CS513ExportTask(CS513SqlTask):
    table_name: str
    export_path: str

    def __init__(self, *, config: dict[str, Any], table_name: str, export_path: str):
        super().__init__(config)
        self.table_name = table_name
        self.export_path = export_path
    
    def run(self) -> Self:
        super().run()
        engine = self.sql_engine
        query = f"SELECT * from {self.table_name}"

        df = pd.read_sql_query(query, engine)
        df.to_csv(self.export_path  , index=False)
        return self

