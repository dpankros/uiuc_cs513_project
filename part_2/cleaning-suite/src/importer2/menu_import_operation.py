from operation import OpenRefineOperation
from openrefine import Server, Project


class MenuImportOperation(OpenRefineOperation):
    def run(self):
        super().run()
        source_filename = self.config['source_filename']
        dest_filename = self.config['dest_filename']
        server_url = self.config['server_url']

        assert(source_filename, "source_filename is required")
        assert(dest_filename, "dest_filename is required")

        server = self.server

        project = server.create_project_from_file(source_filename, 'Menu')


        name_op = [
            {
                "op": "core/column-addition",
                "engineConfig": {
                    "facets": [],
                    "mode": "row-based"
                },
                "baseColumnName": "name",
                "expression": 'grel:value.trim().toLowercase().replace(/[\\[\\]]/, "")',
                "onError": "set-to-blank",
                "newColumnName": "norm_name",
                "columnInsertIndex": 2,
                "description": "Standardize delimiters and remove hard backets"
            }

        ]
        project.apply_operations(name_op)

        # event_replace_ops = [
        #     [",", ";"],
        #     [/;$/, ""]
        # ]

        event_expression = '.'.join([
            'value',
            'trim()',
            'toLowercase()',
            'replace(",", ";")', # change all comma delimiters to semicolon  BUT SEE 24787
            'replace(/;$/, "")', # remove extra hanging delimiters
            'replace(/\\(\\?(.+)\\?\\)/,"$1")', # change (something) to something
            'replace(/\\[\\(\\](.+)[\\]\\)]\\)/,"$1")', # change ^(something)$ OR ^[something]$ to something
            'replace(/([0-9]?[0-9]);([0-9][0-9])/, "$1:$2")', # change 3;00 to 3:00 (normalize times)
            'replace(/[\\[\\]]/, "")', # remove hard brackets
            'replace(/\\?$/,"")',  # change foo? to foo  (and all instances of just "?")
            'replace(/\\?;/,"")',  # change something?; something to something; something
            'replace(/^\'/,"")',  # change 'something to something
            'trim()'
        ])
        event_op = [
            {
                "op": "core/column-addition",
                "engineConfig": {
                    "facets": [],
                    "mode": "row-based"
                },
                "baseColumnName": "event",
                "expression": f'grel:{event_expression}',
                "onError": "set-to-blank",
                "newColumnName": "norm_event",
                "columnInsertIndex": 5,
                "description": "Standardize delimiters and remove hard backets"
            }

        ]
        project.apply_operations(event_op)

        # op = [
        #     {
        #         "op": "core/column-addition",
        #         "engineConfig": {
        #             "facets": [],
        #             "mode": "row-based"
        #         },
        #         "baseColumnName": "name",
        #         "expression": 'grel:value.trim().toLowercase().replace(\" & \",\" and \").replace(/[\\;\\:\\.\\,\\>\\<\\/\\?\\[\\]\\{\\}\\(\\)\\*\\&\\^\\%\\$\\#\\@\\!\\-\\+\\=\\_]/, \"\")',
        #         "onError": "set-to-blank",
        #         "newColumnName": "norm_event",
        #         "columnInsertIndex": 2,
        #         "description": "Create column norm_name"
        #     }
        #
        # ]
        # # create the norm_name column
        # project.apply_operations(op)

        # cluster on 'norm_name'
        project.cluster_column('name')
        project.cluster_column('sponsor')


        project.export_rows(dest_filename)
