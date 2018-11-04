import inspect


class CheckerSpaces:
    def __init__(self):
        self.open_bracket = ['(', '{', '[']
        self.close_bracket_and_special_chars = [')', '}', ']', ',', ';', ':']
        self.operators = ['-', '+', '==', '*', '^', '%', '/', '!', '>', '<',
                          'd', 'r', ' ']
        self.checkers = []
        for s in dir(self):
            if inspect.ismethod(getattr(self, s)) and s.startswith("_check"):
                self.checkers.append(getattr(self, s))

    def _check_space_in_end(self, line, vars):
        """
            Метод проверяет наличие пробельных символов в конце строки
        """
        if len(line) != 0:
            if line[:-1].endswith(" ") or line.endswith(" \n") or\
                    line.endswith("\t"):
                return [(vars.line_counter, len(line)),
                        " W291 trailing whitespace"]

    def _check_two_spaces_before_comment(self, line, vars):
        """
            Метод проверяет наличие двух пробелов перед однострочным
            комментарием, который находтися не в начале строки
        """
        index = line.find("#")
        if index != -1:
            if line[index + 1] != " ":
                return [(vars.line_counter, index),
                        " E261 block comment should start with '#'"]

    def _check_spases_around_keyword_or_equals_parameter(self, line, vars):
        """
            Прверяет пробелы возле знаков =, >, <, ! в выражениях
        """
        for char in ['=', '>', '<', '!']:
            index = line.find(char)
            if index == -1 or 'def' in line:
                return None
            if (line[index - 1] != " " or line[index + 1] != " ") and \
                    line[index + 1] != "=" and line[index - 1] != "=" and \
                    line[index - 1] != "!" and line[index - 1] != "<" and \
                    line[index - 1] != ">":
                return [(
                    vars.line_counter, index
                ), " E251 unexpected spaces around keyword / parameter equals"]

    def _check_mult_four_ident(self, line, vars):
        copy_line = line
        index = 0
        while copy_line[0] == ' ':
            index += 1
            copy_line = copy_line[1:]
            if copy_line == "":
                break
        if index % 4 != 0:
            return [(vars.line_counter, 1),
                    " E111 indentation is not a multiple of four"]

    def _check_space_around_operatr(self, line, vars):
        errors = []
        operators = ['-', '+', '*', '^', '%', '/']
        for index in range(len(line)):
            # if line[index] in operators and line[index+1] != ' ':
            #    err_str = " E201 whitespace after " + line[index]
            #    errors.append([(vars.line_counter, index), err_str])
            if line[index-1] != ' ' and line[index] in operators:
                err_str = " E211 whitespace before " + line[index]
                errors.append([(vars.line_counter, index), err_str])
        return errors if len(errors) != 0 else None

    def _check_exp_unexp_ident(self, line, vars):
        """
        проверка отступов
        """
        res = None
        count_indent = vars.in_class+vars.in_method+vars.in_bracket
        if count_indent > 0:
            prefix = '    ' * count_indent
            if not line.startswith(prefix) and line != '\n':
                res = [(vars.line_counter, 1),
                       " E112 expected an indented block"]
        # else:
        #    if line.startswith(' '):
        #        res = [(vars.line_counter, 5), " E113 unexpected indentation"]
        return res

    def _check_space_around_bracket_and_special_chars(self, line, vars):
        errors = []
        for index in range(len(line)):
            if line[index] in self.open_bracket and line[index+1] == ' ':
                err_str = " E201 whitespace after " + line[index]
                errors.append([(vars.line_counter, index), err_str])
            # if line[index] == ' ' and \
            # line[index+1] in self.close_bracket_and_special_chars:
            #    err_str = " E211 whitespace before " + line[index+1]
            #    errors.append([(vars.line_counter, index), err_str])
        return errors if len(errors) != 0 else None
