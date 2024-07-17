from operation import OpenRefineOperation
from openrefine import Server, Project
from openrefine.operations import ColumnAdditionOp, OnErrorTypes


class MenuImportOperation(OpenRefineOperation):
    NO_HANGING_DELIMITER = 'replace(/;\\s*$/, "")'
    NO_DOUBLE_SPACES = 'replace(/\\s+/, " ")'
    SPACED_DELIMITERS = 'replace(/;/, "; ")'

    def run(self):
        super().run()
        source_filename = self.config['source_filename']
        dest_filename = self.config['dest_filename']
        server_url = self.config['server_url']
        sql_engine = self.config['sql_engine']

        assert source_filename, "source_filename is required"
        assert dest_filename is not None or sql_engine is not None, "dest_filename or a sql_engine is required"

        server = self.server

        project = server.create_project_from_file(source_filename, 'Menu')

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
        event_expression = '.'.join([
            'value',
            'trim()',
            'toLowercase()',
            'replace(",", ";")',  # change all comma delimiters to semicolon  BUT SEE 24787, 13546, 13975
            'replace(" & ", "; ")',  # change all foo & bar to foo; bar
            'replace(" and ", "; ")',  # change all foo & bar to foo; bar 14159
            'replace(" and/or ", "; ")',  # change all foo and/or bar to foo; bar 13553
            'replace("/", "; ")',  # change all breakfast/supper/lunch to breakfast; supper; lunch
            'replace("(?)", "")',  # remove (?) 14076, 14078
            'replace(/;$/, "")',  # remove extra hanging delimiters
            'replace(/\\(\\?(.+)\\?\\)/,"$1")',  # change (something) to something
            'replace(/\\[\\(\\](.+)[\\]\\)]\\)/," $1 ")',  # change ^(something)$ OR ^[something]$ to something
            'replace(/([0-9]?[0-9]);([0-9][0-9])/, "$1:$2")',  # change 3;00 to 3:00 (normalize times)
            'replace(/[\\[\\]]/, " ")',  # remove hard brackets
            'replace(/\\?\\s*$/,"")',  # change foo? to foo  (and all instances of just "?") 14408
            'replace(/\\?;/,"")',  # change something?; something to something; something
            'replace(/^\'/,"")',  # change 'something to something
            'replace(/\\s*;\\s*/,"; ")',  # normalize delimiter spaces, like in 13553, 13563
            'replace(/\\s+/," ")',  # all spaces are at most 1
            'trim()'
        ])
        sponsor_expression = '.'.join([
            'value',
            'trim()',
            'toTitlecase()'
        ])
        place_expression = '.'.join([
            'value',
            'trim()',
            'toLowercase()',
            'replace(/"\\s*([\\w,.-]+\\s*)"/, "\\"$1\\"")',
            # remove spaces at the beginning of a quoted string e.g. 12527 vs 12528
            'replace(/[\\[\\(]/, ", ")',  # 12490
            'replace(/[\\]\\)]/, "")',  # 12490
            'replace(",", ", ")',
            'replace(/\\?\\s*$/, "")',  # e.g. 12518, 12490
            self.NO_HANGING_DELIMITER,  # remove extra hanging delimiters
            'replace(/\\s+,/,",")',  # remove spaces before commas
            'replace(/,+/,",")',  # remove reduntant commas e.g. 12474
            'replace(/^\\s*,\\s*/,"")',  # remove starting commas e.g. 12490, 12578
            self.NO_DOUBLE_SPACES,  # all spaces are at most 1
            'trim()',
            'toTitlecase()'
        ])
        physical_description_expression = '.'.join([
            'value',
            'trim()',
            'toLowercase()',
            'replace(/([\\d]+(\\.[\\d]{1,2})?)\\s+x\\s+([\\d]+(\\.[\\d]{1,2})?)/, "$1x$3")',  # e.g. 23965
            self.SPACED_DELIMITERS,
            self.NO_DOUBLE_SPACES,  # all spaces are at most 1
            self.NO_HANGING_DELIMITER,  # remove extra hanging delimiters
            'replace(/ ill(;|$)/, " illus$1")',
            'trim()'
        ])

        project.apply_operations([
            ColumnAdditionOp(base_column_name='physical_description', new_column_name='norm_physical_description',
                             column_insert_index=7,
                             expression=physical_description_expression).value(),
            ColumnAdditionOp(base_column_name='place', new_column_name='norm_place', column_insert_index=6,
                             expression=place_expression).value(),
            ColumnAdditionOp(base_column_name='venue', new_column_name='norm_venue', column_insert_index=5,
                             expression=venue_expression).value(),
            ColumnAdditionOp(base_column_name='event', new_column_name='norm_event', column_insert_index=4,
                             expression=event_expression).value(),
            ColumnAdditionOp(base_column_name='sponsor', new_column_name='norm_sponsor', column_insert_index=3,
                             expression=sponsor_expression).value(),
            ColumnAdditionOp(base_column_name='name', new_column_name='norm_name', column_insert_index=2,
                             expression='value.trim().toLowercase().replace(/[\\[\\]]/, "")').value(),

        ])

        # temporarilty removed for speed
        # project.cluster_column('name')
        # project.cluster_column('sponsor')

        self.export(project)
