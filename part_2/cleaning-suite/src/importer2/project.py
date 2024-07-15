import requests
import re
import urllib.parse
import json
import io
import functools


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

    def export_rows(self, filename='data.csv', format="csv"):
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
        with open(filename, 'w') as file:
            file.write(content)
        return content

    def cluster_column(self, column: str):
        # [ [{ v: "str VALUE", "c": int count? }, { v: "str VALUE", "c": int count? }, ...], ... ]
        cluster_data = self.compute_clusters(column)
        # [ {from: ["str", "str"], "to": "str"}, ...]
        mass_edit_data = []
        # print(f"Cluster Data: {cluster_data}")
        for cluster_list in cluster_data:
            # print(f"Cluster List: {cluster_list}")
            to_value = cluster_list[0]['v']
            from_values = [value['v'] for value in cluster_list]
            mass_edit_data.append({'from': from_values, 'to': to_value})

        r = self.mass_edit(column, edits=mass_edit_data)
        if not r['code'] == 'ok':
            # print(r)
            raise Exception(f"Cluster failed: {r['message']}")

        return self

