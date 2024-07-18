from importer2.open_refine_operation import OpenRefineOperation


class CS513ImportOperation(OpenRefineOperation):
    #
    # Common grel expressions for all CS513 import operations
    #
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
