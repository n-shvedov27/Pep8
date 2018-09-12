"""
    Модуль для хранения констант
"""
SPECIAL_CHARACTERS = ['-', '+', '=', '*',
                      '^', '%', '/', '!', '>', '<',
                      'd', 'r', ' ']
_OPERATORS = ['-', '+', '=', '*',
              '^', '%', '/', '!', '>', '<']
MAX_LENGTH = 79
LENGTH = " E501 line too long("
SPACE_IN_END = " W291 trailing whitespace"
TWO_SPACES_BEFORE_COMMENT = " E261 at least two spaces before inline comment"
SPACE_IN_BRACKETS = " whitespace "
IF = " continuation line does not distinguish itself from next logical line"
MULT_IMPORT = " E401 multiple imports in one line"
SPACES_AROUND_KEYWORD = " E251 unexpected spaces around keyword /" +\
    "parameter equals"
TABS = " W191 indentation contains tabs"
MIXT = " E101 indentation contains mixed spaces and tabs"
MULT_FOUR_IDENT = " E111 indentation is not a multiple of four"
EXP_ID_BLOCK = " E112 expected an indented block"
UNEXP_ID_BLOCK = " E113 unexpected indentation"
UNDER_IDENT = " E128 continuation line under - indented for visual indent"
OVER_IDENT = " E127 continuation line over - indented for visual indent"
TWO_BLANK_LINES = " E302 expected 2 blank lines, found "
TOO_MANY_BLANK_LINES = " E303 too many blank lines("
OPERATORS = " E255 missing spaces around operator"
OPER_MULT_B = " E221 multiple spaces before operator"
OPER_MULT_A = " E222 multiple spaces after operator"
OPER_TAB_B = " E223 tab before operator"
OPER_TAB_A = " E224 tab before operator"
COLON = " E203 whitespace before ':'"
COMMA = " E231 missing whitespace after ', '"
LAST_LINE = " W292 no new line at end of file"
BLANK_LINE = " W391 blank line at end of file"
BLANK_LINE_WITH_WHITESPACE = " W293 blank line contains whitespace"
BLANK_LINE_DECORATOR = " E304 blank lines found after function decorator"
