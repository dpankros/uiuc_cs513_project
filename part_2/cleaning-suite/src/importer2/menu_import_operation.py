from operation import OpenRefineOperation
from openrefine import Server, Project


class MenuImportOperation(OpenRefineOperation):
    def run(self):
        super().run()
        source_filename = self.config['source_filename']
        dest_filename = self.config['dest_filename']
        server_url = self.config['server_url']
        sql_engine = self.config['sql_engine']

        assert(source_filename, "source_filename is required")
        assert(dest_filename is not None or sql_engine is not None, "dest_filename or a sql_engine is required")

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

        venue_expression = '.'.join([
            'value',
            'trim()',
            'toLowercase()',
            'replace(",", ";")',
            'replace("commercial", "com")',
            'replace("railroad", "rail")',
            'replace("social", "soc")',
            'replace("soc club", "soc")',
            'replace("education", "educ")',
            'replace("millitary", "mil")',
            'replace("navy", "nav")',
            'replace("polictical", "pol")',
            'replace("government", "gov")',
            'replace("professional", "prof")',
            'replace("religious", "relig")',
            'replace("musical", "mus")',
            'replace("hotel", "hot")',
            'replace("restaurant", "rest")',
            'replace("foreign", "for")',
            'replace("steamship", "steam")',
            # TODO : I've taken a stab at calssifying the straggler "other" types, but a few remain (11 rows in total)
            # some could probable be converted into the above groups or made into their own
            # e.g.
            # ```sql
            # select norm_venue, count(norm_venue) as count from menu
            # where norm_venue like 'other%' group by norm_venue order by count desc;
            # ```
            'replace(/^other[^\\w]+([\\w\\s\\-;]+)[^\\w]*$/, "other - $1")',
            'replace("other - soc", "soc")',
            'replace("other - private party", "priv")',
            'replace("other - private", "priv")',
            'replace("other - privately hosted dinner party", "priv")',
            'replace("other - private hosts", "priv")',
            'replace("other - individual", "priv")',
            'replace("other - group of citizens", "priv")',
            'replace("other - group of friends", "priv")',
            'replace(/other - .*privat.+/, "priv")',
            'replace("other - personal", "priv")',
            'replace("other - residence", "priv")',
            'replace("other - theater", "mus")',
            'replace("other - hospital", "med")',
            'replace(/other - sport.*/, "sport")',
            'replace(/other - .*royal.*/, "royal")',
            'replace(/other - .*club.*/, "club")',  # should this be soc?
            'replace(/other - .*trade.*/, "com")',
            'replace("other - private club", "club")',
            'replace("(?)", " ")',
            'replace("?", " ")',

            'replace(/;$/, "")',  # remove extra hanging delimiters
            'replace(/\\s*;\\s*/,"; ")',  # normalize delimiter spaces
            'replace(/\\s+/," ")',  # all spaces are at most 1
            'trim()'
        ])
        venue_op = [
            {
                "op": "core/column-addition",
                "engineConfig": {
                    "facets": [],
                    "mode": "row-based"
                },
                "baseColumnName": "venue",
                "expression": f'grel:{venue_expression}',
                "onError": "set-to-blank",
                "newColumnName": "norm_venue",
                "columnInsertIndex": 6,
                "description": "Standardize delimiters and remove hard backets"
            }

        ]
        project.apply_operations(venue_op)

        event_expression = '.'.join([
            'value',
            'trim()',
            'toLowercase()',
            'replace(",", ";")', # change all comma delimiters to semicolon  BUT SEE 24787, 13546, 13975
            'replace(" & ", "; ")', # change all foo & bar to foo; bar
            'replace(" and ", "; ")', # change all foo & bar to foo; bar 14159
            'replace(" and/or ", "; ")', # change all foo and/or bar to foo; bar 13553
            'replace("/", "; ")', # change all breakfast/supper/lunch to breakfast; supper; lunch
            'replace("(?)", "")', # remove (?) 14076, 14078
            'replace(/;$/, "")', # remove extra hanging delimiters
            'replace(/\\(\\?(.+)\\?\\)/,"$1")', # change (something) to something
            'replace(/\\[\\(\\](.+)[\\]\\)]\\)/," $1 ")', # change ^(something)$ OR ^[something]$ to something
            'replace(/([0-9]?[0-9]);([0-9][0-9])/, "$1:$2")', # change 3;00 to 3:00 (normalize times)
            'replace(/[\\[\\]]/, " ")', # remove hard brackets
            'replace(/\\?\\s*$/,"")',  # change foo? to foo  (and all instances of just "?") 14408
            'replace(/\\?;/,"")',  # change something?; something to something; something
            'replace(/^\'/,"")',  # change 'something to something
            'replace(/\\s*;\\s*/,"; ")',  # normalize delimiter spaces, like in 13553, 13563
            'replace(/\\s+/," ")',  # all spaces are at most 1
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

        self.export(project)
