import math
from dataclasses import dataclass

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Connection

from importer2.task import SqlTask


@dataclass
class BeforeAndAfter:
    before: float
    after: float
    improvement: float

nullResult = BeforeAndAfter(before=math.nan, after=math.nan, improvement=math.nan)

@dataclass
class StatsObject:
    count: BeforeAndAfter
    min: BeforeAndAfter
    max: BeforeAndAfter
    avg: BeforeAndAfter


class CS513ReportTask(SqlTask):
    column_mapping = {
        # base_col: view_col
        "id": "id",
    }
    stat_columns = {
        # "column": { type: "stat_function" ....}
    }
    base_table: str = None
    comparison_table: str = None
    base_table_pk: str = "id"
    comparison_table_pk: str = "id"

    # column: [ constraint, constraint...] OR
    # column: constraint
    integrity_constraints: dict = {}
    # the foreign keys from the base table.
    # key: foreign_table
    foreign_keys = {}

    def __init__(self, operation_config: dict = {}):
        super().__init__(operation_config)
        self.max_count: int = operation_config.get('max_count', 10)
        # self.table = operation_config.get('table', None)
        self.before_table: str = operation_config.get('base_table', None)
        self.comparison_table: str = operation_config.get('comparison_table', None)

    def standard_stats(self, before_col_name: str, after_col_name: str) -> StatsObject:
        sql_query = lambda c, t: f"select count(distinct {c}) as count from {t}"
        with self.sql_engine.connect() as conn:
            before_count = conn.execute(text(sql_query(before_col_name, self.base_table))).fetchone()[0]
            after_count = conn.execute(text(sql_query(after_col_name, self.comparison_table))).fetchone()[0]

        # before, after, % improvement

        before_count = max(1, before_count)
        stats = StatsObject(
            count=BeforeAndAfter(
                before=before_count,
                after=after_count,
                improvement=100.0 * (before_count - after_count) / before_count
            ),
            min=nullResult,
            max=nullResult,
            avg=nullResult,
        )
        return stats

    def multi_valued_stats(self, before_col_name, after_col_name):

        sql_query = lambda c, t: f"""
WITH RECURSIVE SplitValues AS (
    SELECT
        id,
        TRIM(SUBSTR({c} || ';', 1, INSTR({c} || ';', ';') - 1)) AS value,
        TRIM(SUBSTR({c} || ';', INSTR({c} || ';', ';') + 1)) AS remaining
    FROM
        {t}
    UNION ALL
    SELECT
        id,
        TRIM(SUBSTR(remaining, 1, INSTR(remaining, ';') - 1)),
        TRIM(SUBSTR(remaining, INSTR(remaining, ';') + 1))
    FROM
        SplitValues
    WHERE
        remaining != ''
)
SELECT value, COUNT(*) as count
FROM SplitValues
WHERE value != ''
GROUP BY value
ORDER BY count desc;        
        """
        with self.sql_engine.connect() as conn:
            # format is:
            # value | count
            # ... for each delimited value in the column ...
            before_count = len(conn.execute(text(sql_query(before_col_name, self.base_table))).fetchall())
            after_count = len(conn.execute(text(sql_query(after_col_name, self.comparison_table))).fetchall())

        # before, after, % improvement

        before_count = max(1, before_count)
        stats = StatsObject(
            count=BeforeAndAfter(
                before=before_count,
                after=after_count,
                improvement=100.0 * (before_count - after_count) / before_count
            ),
            min=nullResult,
            max=nullResult,
            avg=nullResult,
        )
        return stats

    def numeric_stats(self, before_col_name, after_col_name):
        sql_query = lambda c, t: f"select min({c}), max({c}), avg({c}), count({c}) from {t}"
        with self.sql_engine.connect() as conn:
            before_min, before_max, before_avg, before_count = conn.execute(text(sql_query(before_col_name, self.base_table))).fetchone()
            after_min, after_max, after_avg, after_count = conn.execute(text(sql_query(after_col_name, self.comparison_table))).fetchone()

        # before, after, % improvement

        before_count = max(1, before_count)
        stats = StatsObject(
            count=BeforeAndAfter(
                before=before_count,
                after=after_count,
                improvement=100.0 * (before_count - after_count) / before_count
            ),
            min=BeforeAndAfter(
                before=before_min,
                after=after_min,
                improvement=math.nan,
            ),
            max=BeforeAndAfter(
                before=before_max,
                after=after_max,
                improvement=math.nan,
            ),
            avg=BeforeAndAfter(
                before=before_avg,
                after=after_avg,
                improvement=math.nan,
            ),
        )
        return stats

    def fk_stats(self, before_col_name, after_col_name):
        # for each FK column, we expect to have more NULL values in 
        # self.comparison_table than in self.base_table
        comparison_query = f"select count(*) from {self.comparison_table} as m where m.{after_col_name} is NULL"
        base_query = f"select count(*) from {self.base_table} as m where m.{after_col_name} is NULL"
        with self.sql_engine.connect() as conn:
            after_count = conn.execute(text(comparison_query)).fetchone()[0]
            before_count = conn.execute(text(base_query)).fetchone()[0]
            before_count = max(1, before_count)
            stats = StatsObject(
                count=BeforeAndAfter(
                    before=float(before_count),
                    after=float(after_count),
                    improvement=(float(after_count) / float(before_count)) * 100
                ),
                min=nullResult,
                max=nullResult,
                avg=nullResult,
            )
            return stats

    def run(self):
        self.connection: Connection = self.sql_engine.connect()

        all_violations = {}
        violation_cols = {}
        try:
            with self.connection as conn:
                if len(self.integrity_constraints.keys()) > 0:
                    data = pd.read_sql(
                        f"select {', '.join(self.integrity_constraints.keys())} from {self.comparison_table}", conn)

                    for index, row in data.iterrows():
                        for col_index, col in enumerate(data.columns):
                            constraint = self.integrity_constraints[col]
                            violations = constraint.check(
                                col,  # column name
                                getattr(row, col),  # column value
                                {  # context object
                                    "row": row,
                                    "table_name": self.comparison_table,
                                    "connection": conn,
                                    "data": data,
                                    "foreign_table": self.foreign_keys.get(col, None)
                                }
                            )
                            if violations is not None:
                                all_violations[index] = violations
                                violation_cols[col] = violation_cols.get(col, 0) + 1

                GROUPS = ['count', 'min', 'max', 'avg']
                print(f"  Column Stats for {self.comparison_table} compared to {self.base_table}")
                group_headers = ''.join([f"{g.title():>5} Before {g.title():>5} After  {g.title():>5} Impr" for g in GROUPS])
                print(f"                  Column {group_headers}")

                for before_col, stat_obj in self.stat_columns.items():
                    after_col = self.column_mapping[before_col]
                    stat_func = stat_obj.get('type', "standard_stats")
                    if not hasattr(self, stat_func):
                        raise Exception(
                            f"Invalid Statistic function {stat_func} for column {self.base_table}.{before_col}")

                    stat_obj = getattr(self, stat_func)(before_col, after_col)
                    stat_str = ""
                    for group_name in GROUPS:
                        group:BeforeAndAfter = getattr(stat_obj, group_name)
                        stat_str += f"{group.before:>11.1f} {group.after:>11.1f} {group.improvement:>10.1f}%"
                    # print(f"    {before_col:>10}: {before:>10} {after:>10} ({improvement:>6.1f}%)")
                    print(f"    {before_col:>20}  {stat_str}")

            print(f"  {len(all_violations.keys())} Rows with databse IC violations")

            if len(all_violations.keys()) > 0:
                cols_strs = []
                for key, count in violation_cols.items():
                    cols_strs.append(f"{key} ({count})")
                print(f"  Errors were detected in the following columns: {', '.join(cols_strs)}")
        finally:
            self.connection.close()
