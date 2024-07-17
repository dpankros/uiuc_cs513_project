import requests
import re
import urllib.parse
import json
import io
import functools
import pandas as pd
from io import StringIO


class Project:
    def __init__(self, id: int, server=None):
        if not id:
            raise Exception('Invalid project id')

        self.id = id
        self.server: Server = server

    def __repr__(self):
        return f"Project(id={self.id}; server={self.server.url})"

    def get_models(self):
        return self.server.get(
            'command/core/get-models',
            query={'project': self.id}
        ).json()

    def get_project_url(self):
        return f"{self.server.url}/project?project={self.id}"

    def apply_operations(self, operations_json: list):
        try:
            r = self.server.post(
                'command/core/apply-operations',
                query={'project': self.id},  # the docs say this is where it belongs, but reality says it's in the data
                data={
                    'project': self.id,
                    'operations': json.dumps(operations_json)
                }
            ).json()
        except Exception as e:
            raise Exception(f"Apply Operations failed") from e

        if not r['code'] == 'ok':
            raise Exception(f"Apply Operations failed: {r['message']}")

        return self

    def get_history(self):
        return self.server.get(
            'command/core/get-history',
            query={'project': self.id}
        ).json()

    def get_rows(self, start=0, limit=50):
        return self.server.get(
            'command/core/get-rows',
            query={
                'project': self.id,
                'start': start,
                'limit': limit,
            }
        ).json()

    def compute_facets(self, column: str):
        r = self.server.post(
            'command/core/compute-facets',
            query={'project': self.id},  # the docs say this is where it belongs, but reality says it's in the data
            data={
                "engine": json.dumps({
                    "facets": [
                        {
                            "type": "list",
                            "name": column,
                            "columnName": column,
                            "expression": "value",
                            "omitBlank": False,
                            "omitError": False,
                            "selection": [],
                            "selectBlank": False,
                            "selectError": False,
                            "invert": False
                        }
                    ],
                    "mode": "row-based"
                })}
        ).json()

        errors = functools.reduce(lambda a, v: [*a, v['error']] if v['error'] else a, r['facets'], [])

        if len(errors) > 0:
            raise Exception(f"Compute Facets Failed: {';'.join(errors)}")

        return self

    def compute_clusters(self, column: str, function: str = 'fingerprint', type: str = 'binning', params: map = {}):
        return self.server.post(
            'command/core/compute-clusters',
            query={'project': self.id},  # the docs say this is where it belongs, but reality says it's in the data
            data={
                "engine": json.dumps({
                    "facets": [],
                    "mode": "row-based"
                }),
                "clusterer": json.dumps({
                    "type": type,
                    "function": function,
                    "column": column,
                    "params": params
                })
            }
        ).json()

    def mass_edit(self, column: str, edits: list = []):
        return self.server.post(
            'command/core/mass-edit',
            query={'project': self.id},  # the docs say this is where it belongs, but reality says it's in the data
            data={
                "columnName": column,
                "expression": "value",
                "edits": json.dumps(edits),
                "engine": json.dumps({"facets": [], "mode": "row-based"})
            }
        ).json()

    def export_rows(self, format="csv"):
        """
        Exports the project data to a string in the specified format
        :param format: csv or tsv (or anything that the export-rows operation of openrefine accepts)
        :return: the exported string
        """
        content = self.server.post(
            'command/core/export-rows',
            query={
                'project': self.id,
                'format': 'csv'
            },
            data={
                "engine": json.dumps({"facets": [], "mode": "row-based"})
            }
        ).text

        return content

    def export_rows_to_file(self, filename='data.csv', format="csv"):
        """
        Write the project data to a file
        :param filename: the name/path of the file
        :param format: a format, such as csv or tsv
        :return: self for chaining
        """
        content = self.export_rows(format)
        with open(filename, 'w') as file:
            file.write(content)
        return self

    def to_df(self):
        """
        Export the data in the project to a pandas dataframe
        :return:
        """
        dio = StringIO(self.export_rows('csv'))
        return pd.read_csv(dio)

    def to_sql(self, sql_engine, table_name='new_table', if_exists='fail'):
        """
        Export the data in the project to a sqlite database
        :param sql_engine: a sqlalchemy engine i.e. `create_engine('sqlite:///my_sqlite.db')`
        :param table_name: the name of the table to export to within the database
        :return: self for chaining
        """
        df = self.to_df()
        df.to_sql(table_name, con=sql_engine, index=False, if_exists=if_exists)
        return self

    def cluster_column(self, column: str):
        # [ [{ v: "str VALUE", "c": int count? }, { v: "str VALUE", "c": int count? }, ...], ... ]
        cluster_data = self.compute_clusters(column)
        # [ {from: ["str", "str"], "to": "str"}, ...]
        mass_edit_data = []
        # print(f"Cluster Data: {cluster_data}")
        for cluster_list in cluster_data:
            # print(f"Cluster List: {cluster_list}")
            to_value = \
            functools.reduce(lambda result, v: v if v['c'] > result['c'] else result, cluster_list, {'c': 0, 'v': ''})[
                'v']
            from_values = [value['v'] for value in cluster_list]
            if len(to_value) > 0:
                mass_edit_data.append({'from': from_values, 'to': to_value})

        r = self.mass_edit(column, edits=mass_edit_data)
        if not r['code'] == 'ok':
            # print(r)
            raise Exception(f"Cluster failed: {r['message']}")

        return self
