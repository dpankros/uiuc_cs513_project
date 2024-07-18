from importer2.task import OpenRefineTask


class CS513ImportTask(OpenRefineTask):
  #
  # Common grel expressions for all CS513 import operations
  #
  TO_ISO8601_EXTDATE='replace(/(\\d{2,4})-(\\d{1,2})-(\\d{1,2})\\s+(\\d{1,2}):(\\d{1,2}):(\\d{1,2})\\s+UTC/, "$1-$2-$3T$4:$5:$6Z")'
  TO_ISO8601_DATE='replace(/(\\d{2,4})-(\\d{1,2})-(\\d{1,2})\\s+(\\d{1,2}):(\\d{1,2}):(\\d{1,2})\\s+UTC/, "$1$2$3T$4$5$6Z")'
  USE_SEMI_DELIMITERS = 'replace(",", ";")'
  NO_HANGING_DELIMITER = 'replace(/;\\s*$/, "")'
  NO_DOUBLE_SPACES = 'replace(/\\s+/, " ")'
  SPACED_DELIMITERS = 'replace(/\\s*;\\s*/,"; ")'  # 'replace(/;/, "; ")'
  SPACE_AFTER_COMMA = 'replace(",", ", ")'
  OPEN_BRACKETS_TO_COMMA = 'replace(/[\\[\\(\\{]/, ", ")'
  NO_OPEN_BRACKETS = 'replace(/[\\[\\(\\{]/, " ")'
  NO_SPACE_BEFORE_COMMAS = 'replace(/\\s+,/,",")'
  NO_CLOSE_BRACKETS = 'replace(/[\\]\\)\\}]/, "")'
  NO_STARTING_COMMAS = 'replace(/^\\s*,+\\s*/,"")'
  NO_ENDING_COMMAS = 'replace(/\\,+\\s*$/, "")'
  NO_ENDING_QUESTIONS = 'replace(/\\?+\\s*$/, "")'
  NO_MULTI_COMMAS = 'replace(/,+/,",")'
  NO_QUESTION_MARKS = 'replace("?", " ")'
  NO_PAREN_QUESTION_PAREN = 'replace("(?)", " ")'

  def run(self):
    super().run()
    self.source_filename = self.config['source_filename']
    self.dest_filename = self.config['dest_filename']
    self.server_url = self.config['server_url']
    self.sql_engine = self.config['sql_engine']

    assert self.source_filename, "source_filename is required"
    assert self.dest_filename is not None or self.sql_engine is not None, "dest_filename or a sql_engine is required"

    return self

