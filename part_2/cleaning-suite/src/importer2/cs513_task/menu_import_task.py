from importer2.openrefine.operations import ColumnAdditionOp, ColumnRemovalOp

from .cs513_import_task import CS513ImportTask


class MenuImportTask(CS513ImportTask):
  name = "Menu Import"

  def run(self):
    super().run()

    project = self.server.create_project_from_file(self.source_filename, 'Menu')

    venue_expression = '.'.join([
      'value',
      'trim()',
      'toLowercase()',
      self.USE_SEMI_DELIMITERS,
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
      self.NO_PAREN_QUESTION_PAREN,
      self.NO_QUESTION_MARKS,
      self.NO_HANGING_DELIMITER,
      self.SPACED_DELIMITERS,  # normalize delimiter spaces
      self.NO_DOUBLE_SPACES,  # all spaces are at most 1
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
      self.NO_PAREN_QUESTION_PAREN,  # remove (?) 14076, 14078
      self.NO_HANGING_DELIMITER,
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
      self.OPEN_BRACKETS_TO_COMMA,  # 12490
      self.NO_CLOSE_BRACKETS,  # 12490
      self.SPACE_AFTER_COMMA,
      self.NO_ENDING_QUESTIONS,  # e.g. 12518, 12490
      self.NO_ENDING_COMMAS,
      self.NO_HANGING_DELIMITER,  # remove extra hanging delimiters
      self.NO_SPACE_BEFORE_COMMAS,  # remove spaces before commas
      self.NO_MULTI_COMMAS,  # remove reduntant commas e.g. 12474
      self.NO_STARTING_COMMAS,  # remove starting commas e.g. 12490, 12578
      self.NO_DOUBLE_SPACES,  # all spaces are at most 1
      'trim()',
      'toTitlecase()'
    ])
    physical_description_expression = '.'.join([
      'value',
      'trim()',
      'toLowercase()',
      'replace(/([\\d]+(\\.[\\d]{1,2})?)\\s+x\\s+([\\d]+(\\.[\\d]{1,2})?)/, "$1x$3")',  # e.g. 23965
      self.USE_SEMI_DELIMITERS,
      self.NO_DOUBLE_SPACES,  # all spaces are at most 1
      self.NO_HANGING_DELIMITER,  # remove extra hanging delimiters
      'replace(/ ill(;|$)/, " illus$1")',
      'trim()'
    ])

    # TODO: There are a lot of special cases here.  Look at:
    # ```sql
    # select norm_occasion, count(norm_occasion) as count from menu group by norm_occasion order by norm_occasion asc;
    # ```
    occasion_expression = '.'.join([
      'value',
      'trim()',
      'toLowercase()',
      # self.USE_SEMI_DELIMITERS,
      'replace("[", "(")',
      'replace("]", ")")',
      'replace(/other\\s+\\((.+)\\)/, "$1")',
      'replace(/other\\s*,(.+)/, "$1")',
      'replace("other - soc", "soc")',
      'replace("other - social", "soc")',
      'replace("other - daily menu", "daily")',
      'replace("other - daily", "daily")',
      'replace("other - anniversary", "anniversary")',
      'replace("other - anniv", "anniversary")',
      'replace("0ther ", "")',
      'replace(/(ann|aniv|anniv|anniversaryersary)(\\W|$)/, "anniversary$2")',
      self.NO_PAREN_QUESTION_PAREN,
      self.NO_OPEN_BRACKETS,
      self.NO_CLOSE_BRACKETS,
      self.SPACED_DELIMITERS,
      self.NO_DOUBLE_SPACES,  # all spaces are at most 1
      self.NO_HANGING_DELIMITER,  # remove extra hanging delimiters
      self.NO_ENDING_COMMAS,
      self.NO_ENDING_QUESTIONS,
      self.NO_STARTING_COMMAS,
      'trim()'
    ])

    location_expression = '.'.join([
      'value',
      'trim()',
      self.NO_PAREN_QUESTION_PAREN,
      self.NO_OPEN_BRACKETS,
      self.NO_CLOSE_BRACKETS,
      self.NO_HANGING_DELIMITER,
      self.NO_DOUBLE_SPACES,
      'trim()',
    ])

    notes_expression = '.'.join([
      'value',
      'trim()',
      self.NO_PAREN_QUESTION_PAREN,
      self.NO_HANGING_DELIMITER,
      self.NO_DOUBLE_SPACES,
      'trim()',
    ])

    # Columns:
    # [x] id - keep
    # [x] name - update
    # [x] sponsor - update
    # [x] event - update
    # [x] venue - update
    # [x] place - update
    # [x] physical_description  - update (not sure if we need more)
    # [x] occasion - update
    # [x] notes - this shouldn't be changed much, maybe ensure delimiters are correct and eliminate hanging
    # [x] call_number -DNC
    # [x] keywords - removed
    # [x] language - removed
    # [x] date - transform to ISO date?
    # [x] location - remove extra spaces, trailing semis, remove "(?)"
    # [x] location_type
    # [x] currency -OK
    # [x] currency_symbol - OK
    # [x] status - OK as is
    # [x] page_count - keep for now
    # [x] dish_count - keep for now

    project.apply_operations([

      # note that these can be changed to TextTransformationOp to modify IN-PLACE by changing base_column_name to
      # column_name and removing new_column_name and column_insert_index

      ColumnAdditionOp(base_column_name='location', new_column_name='norm_location',
                       column_insert_index=14,
                       expression=location_expression).value(),
      ColumnAdditionOp(base_column_name='notes', new_column_name='norm_notes',
                       column_insert_index=9,
                       expression=notes_expression).value(),
      ColumnAdditionOp(base_column_name='occasion', new_column_name='norm_occasion',
                       column_insert_index=8,
                       expression=occasion_expression).value(),
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

      ColumnRemovalOp(column_name='keywords').value(),
      ColumnRemovalOp(column_name='language').value(),
      ColumnRemovalOp(column_name='location_type').value(),
    ])

    project.cluster_column('norm_name')
    project.cluster_column('norm_sponsor')
    project.cluster_column('norm_occasion')

    self.export(project)
