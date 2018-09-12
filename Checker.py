import re
import inspect

import Const

blank_exp = re.compile(r'^( |\t)+(\n)?$')
dec_exp = re.compile(r'^( )*@(.)*')
ident_exp = re.compile(r'^( )*')
ident = re.compile(r'^( )*(for|while|if|elif|else|def|class|try|except)')


class MainChecker():
    """
        В классе MainChacker реализована проверка строк или файлов
        на соответствие правилам PEP8
    """
    def __init__(self):
        """
            Словарь self.errors хранит списки ошибок.
            Ключом в словаре является имя файла.
            Если обрабатываются строки с stdin, то ключом будет
                строка "stdin".
            Список self.checkers содержит декларации функций проверки
                отдельных правил.
            Переменные self.line_counter номер строки в файле
            self.if_flag флаг, встречалась ли в предыдущей строке
                подстрока "if"
            self.if_length длина вышеуказанной строки, если флаг принимает
                значение истина
            self.blank_lines_counter количество подряд идущих пустых строк
        """
        self.errors = {}
        self.checkers = []
        for s in dir(self):
            if inspect.ismethod(getattr(self, s)) and s.startswith("_check"):
                self.checkers.append(getattr(self, s))
        self.line_counter = 0
        self.if_flag = False
        self.if_length = 0
        self.comment = False
        self.decorator = 0
        self.ident = -1
        self.bool_dec = False
        self.b_stack = []
        self.slash = False
        self.open_br = False
        self.ind_br = -1
        self.blank_lines_counter = 0

    def check_file(self, filelike_object, filename):
        """
            Параметр filename для вывода, filelike_object для чтения
        """
        self.line_counter = 0
        if filename not in self.errors.keys():
            self.errors[filename] = []
            last_line_check = ""
            for line in filelike_object:
                last_line_check = line
                self.line_counter += 1
                result = self.check_line(line, filename)
                if result != []:
                    if isinstance(result[0], str):
                        self.errors[filename].append(result)
                    else:
                        self.errors[filename].extend(result)
            last_check = self.check_last_line(last_line_check)
            blank_lines_check = self.check_blank_line()
            if last_check is not None:
                self.errors[filename].append(last_check)
            if blank_lines_check is not None:
                self.errors[filename].append(blank_lines_check)

    def check_line(self, line, filename="stdin"):
        """
            Строки комментариев не проверяются!
            Строка подаётся на вход всем checker'ам из self.checkers
            Если найдена ошибка, то она добавляется в список
            В формате: [(№строки, №столбца), "строковое описание ошибки"]
        """
        if line.startswith("#") or line.find("re.compile") != -1:
            self.blank_lines_counter = 0
            return []
        result_list = []
        for check in self.checkers:
            result = []
            result = check(line)
            if result is not None:
                if type(result[0]) == tuple:
                    result_list.append(result)
                else:
                    result_list.extend(result)
        if filename == "stdin":
            if filename not in self.errors.keys():
                self.errors[filename] = []
            self.errors[filename].extend(result_list)
            self.line_counter += 1
        if line.endswith("\\"):
            self.slash = True
        else:
            self.slash = False
        return result_list

    def get_errors(self, filename):
        if filename in self.errors.keys():
            return self.errors[filename]
        return None

    def print_errors(self, output):
        """
            Метод для вывода ошибок в поток output
        """
        names = list(self.errors.keys())
        names.sort()
        i = 0
        for filename in names:
            i += 1
            if not self.errors[filename]:
                output.write(filename + " is OK")
                output.write("\n")
            for error in self.errors[filename]:
                output.write(self.make_error_string(filename, *error))
                output.write("\n")
            if len(names) != i:
                output.write("\n")

    def make_error_string(self, filename, line_and_column, error_str):
        """
            Метод для формирования строки с ошибкой
        """
        line_num, column_num = line_and_column
        res = "{0}:{1}:{2}:{3}"
        return res.format(filename, line_num, column_num, error_str)

    def _check_length(self, line):
        """
            Метод проверяет длину строки(не больше 79 символов)
        """
        if len(line) > Const.MAX_LENGTH:
            err_str = (Const.LENGTH + str(len(line)) + " > " +
                       str(Const.MAX_LENGTH) + " characters)")
            return [(self.line_counter, 1), err_str]
        return None

    def _check_space_in_end(self, line):
        """
            Метод проверяет наличие пробельных символов в конце строки
        """
        if len(line) != 0:
            if line.endswith(" ") or line.endswith(" \n") or\
                    line.endswith("\t"):
                return [(self.line_counter, len(line)),
                        Const.SPACE_IN_END]
        return None

    def _check_two_spaces_before_comment(self, line):
        """
            Метод проверяет наличие двух пробелов перед однострочным
            комментарием, который находтися не в начале строки
        """
        index = line.find("#")
        if index != -1:
            if line[index - 2:index] != "  " and line[index - 1] != "\"":
                return [(self.line_counter, index),
                        Const.TWO_SPACES_BEFORE_COMMENT]
        return None

    def _check_space_in_brackets(self, line):
        """
            Прверяет пробелы перед скобками и после них.
            Возвращает лист из листов с ошибками
        """
        brackets_errors = []
        index = line.find("(")
        if index != -1:
            if line[index - 1] == ' ' and\
                    line[index - 2] not in Const.SPECIAL_CHARACTERS:
                err_str = " E211" + Const.SPACE_IN_BRACKETS + "before '('"
                brackets_errors.append([(self.line_counter, index), err_str])
            if index != len(line) - 1 and line[index + 1] == ' ':
                err_str = " E201" + Const.SPACE_IN_BRACKETS + "after '('"
                brackets_errors.append([(self.line_counter, index), err_str])
        for bracket in ["[", "{"]:
            index = line.find(bracket)
            if index != -1 and line[index + 1] == ' ':
                err_str = " E201" + Const.SPACE_IN_BRACKETS + "after '" +\
                    bracket + "'"
                brackets_errors.append([(self.line_counter, index), err_str])
        for bracket in ["]", "}", ")"]:
            index = line.find(bracket)
            if index != -1 and line[index - 1] == ' ':
                err_str = " E202" + Const.SPACE_IN_BRACKETS + "before '" +\
                    bracket + "'"
                brackets_errors.append([(self.line_counter, index), err_str])
        if len(brackets_errors) != 0:
            return brackets_errors
        return None

    def _check_if(self, line):
        """
            Прверяет, что если строка заканчивается на "(" и содержит if,
                то в слежуюшей строке под "(" должен находиться символ ":"
        """
        if self.if_flag:
            if len(line) != self.if_length:
                return [(self.line_counter, len(line) - 1), Const.IF]
        else:
            if len(line) != 0:
                if line[-1] == "(" and "if" in line:
                    self.if_flag = True
                    self.if_length = len(line)
        return None

    def _check_mult_import(self, line):
        """
            Прверяет что в файле нет мультиимпортов
        """
        if line.startswith("import") and "from" not in line and ", " in line:
            return [(self.line_counter, line.find(", ")), Const.MULT_IMPORT]
        return None

    def _check_spases_around_keyword(self, line):
        """
            Прверяет пробелы возле знака = в keyword аргументах
        """
        errors = []
        open_ind = line.find("(")
        close_ind = line.find(")")
        if open_ind != -1 and close_ind != -1:
            index = line.find("=", open_ind + 1, close_ind)
            while index != -1:
                if(line[index - 1] == " " or line[index + 1] == " ") and\
                        line[index + 1] != "=" and line[index - 1] != "=" and\
                        line[index - 1] != "!":
                    errors.append([(self.line_counter, index),
                                  Const.SPACES_AROUND_KEYWORD])
                index = line.find("=", index + 1, len(line))
            if len(errors) != 0:
                return errors
            return None
        if open_ind != -1 and "if" not in line:
            index = line.find("=", open_ind + 1, len(line))
            while index != -1:
                if(line[index - 1] == " " or line[index + 1] == " ") and\
                        line[index + 1] != "=" and line[index - 1] != "=":
                    errors.append([(self.line_counter, index),
                                  Const.SPACES_AROUND_KEYWORD])
                index = line.find("=", index + 1, len(line))
        elif close_ind != -1:
            index = line.find("=", 0, close_ind)
            while index != -1:
                if(line[index - 1] == " " or line[index + 1] == " ") and\
                        line[index + 1] != "=" and line[index - 1] != "=" and\
                        line[index + 2] != "\'" and line[index + 2] != "\"":
                    errors.append([(self.line_counter, index),
                                  Const.SPACES_AROUND_KEYWORD])
                index = line.find("=", index + 1, len(line))
        if len(errors) != 0:
            return errors
        return None

    def _check_tabs(self, line):
        """
            Прверяет наличие табуляции
        """
        index = line.find("\t")
        if index != -1:
            return [(self.line_counter, index), Const.TABS]
        return None

    def _check_mixt(self, line):
        """
            Проверяет пробелы и табуляцию на нахождение в одной строке
        """
        errors = []
        index = line.find("\t")
        while index != -1:
            if line[index + 1] == " " or line[index - 1] == " ":
                errors.append([(self.line_counter, index), Const.MIXT])
            index = line.find("\t", index + 1, len(line))
        if len(errors) != 0:
            return errors
        return None

    def _check_mult_four_ident(self, line):
        """
            Проверяет, что количество пробелов в отступах кратно 4
        """
        o = "[{("
        c = "]})"
        if not self.b_stack:
            for i in range(len(line)):
                if line[i] in o:
                    self.b_stack.append((line[i], i))
                if line[i] in c:
                    if c.index(line[i]) == o.index(self.b_stack[
                            len(self.b_stack) - 1][0]):
                        self.b_stack.pop()
            if len(ident_exp.match(line).group()) % 4 != 0:
                return [(self.line_counter, 1), Const.MULT_FOUR_IDENT]
        return None

    def _check_exp_unexp_ident(self, line):
        """
            Проверяет, на наличие отступов или их отсутствие
        """
        res = None
        n = self.ident
        self.ident = -1
        if n > -1:
            if len(ident_exp.match(line).group()) - n > 4 and self.slash:
                res = [(self.line_counter, n), Const.UNEXP_ID_BLOCK]
            elif len(ident_exp.match(line).group()) - n == 0:
                res = [(self.line_counter, n), Const.EXP_ID_BLOCK]
        mo = ident.match(line)
        if mo is not None:
            self.ident = len(mo.group()) - len(mo.group(2))
        return res

    def _check_exp_under_over_ident(self, line):
        """
            Проверяет, на наличие отступов или их отсутствие
        """
        res = None
        o = "[{("
        c = "]})"
        op = line.find("\"")
        while op != -1:
            cl = line.find("\"", op + 1, len(line))
            if cl != -1:
                line = line.replace(line[op: cl + 1], "")
                op = line.find("\"")
            else:
                break
        if self.ind_br != -1:
            n = self.ind_br + 1
            if len(ident_exp.match(line).group()) > n:
                res = [(self.line_counter, n), Const.OVER_IDENT]
            elif len(ident_exp.match(line).group()) < n:
                res = [(self.line_counter, n), Const.UNDER_IDENT]
        for bracket in o:
            ind = line.find(bracket)
            if ind > -1:
                self.ind_br = ind
                break
        for bracket in o:
            ind = line.find(bracket)
            if ind > -1 and ind < self.ind_br:
                self.ind_br = ind
        for b in c:
            if line.find(b) != -1:
                self.ind_br = -1
        return res

    def _check_two_blank_lines(self, line):
        """
            Прверяет, что перед описанием классса или функции(вне класса)
            есть 2 пустые строки
        """
        if self.decorator == 1:
            self.bool_dec = True
        # Если был декоратор в строчке перед нашей, то мы уже проверили
        if line.startswith("def") and self.bool_dec:
            self.bool_dec = False
            return None
        if len(line) == 0 or line == "\n":
            self.blank_lines_counter += 1
            return None
        n = self.blank_lines_counter
        self.blank_lines_counter = 0
        if line.startswith("class") or self.decorator == 1 or\
                line.startswith("def"):
            if n < 2:
                error_str = (Const.TWO_BLANK_LINES + str(n))
                return [(self.line_counter, 1), error_str]
            elif n > 2:
                error_str = (Const.TOO_MANY_BLANK_LINES + str(n) + ")")
                return [(self.line_counter, 1), error_str]
        return None

    def _check_blank_lines_with_spaces(self, line):
        """
            Прверяет, что пустые строки не содержат пробелов
        """
        if blank_exp.match(line) is not None:
            self.blank_lines_counter += 1
            return [(self.line_counter, 1), Const.BLANK_LINE_WITH_WHITESPACE]
        return None

    def _check_blank_line_after_decorator(self, line):
        """
            Прверяет, что после декоратора нет пустых строк
        """
        if dec_exp.match(line) is not None:
            self.decorator += 1
        elif(len(line) == 0 or line == "\n") and self.decorator > 0:
            self.decorator += 1
        else:
            n = self.decorator
            self.decorator = 0
            if n > 1:
                return [(self.line_counter - 1, 1),
                        Const.BLANK_LINE_DECORATOR]
        return None

    def _check_operators(self, line):
        """
            Прверяет пробелы вокруг знаков операций
            Знаки табуляции и множественные прбелы
        """
        errors = []
        for i in range(len(line) - 2):
            before = line[i - 1]
            after = line[i + 1]
            if line[i] in Const._OPERATORS:
                if(before != ' ' or after != ' ') and\
                        before != "'" and after != "'" and before != '"' and\
                        after != '"' and line[i] != '=' and\
                        after != '=' and before not in ["(", "[", "{"] and\
                        not after.isdigit() and not line[i] == "*" and\
                        not after.isalpha() and after != "\\":
                    errors.append([(self.line_counter, i), Const.OPERATORS])
                if line[i - 2:i] == "  ":
                    errors.append([(self.line_counter, i), Const.OPER_MULT_B])
                if line[i + 1:i + 3] == "  ":
                    errors.append([(self.line_counter, i), Const.OPER_MULT_A])
                if before == "\t":
                    errors.append([(self.line_counter, i), Const.OPER_TAB_B])
                if after == "\t":
                    errors.append([(self.line_counter, i), Const.OPER_TAB_A])
            if line[i - 1].isdigit() and line[i] == "=" and\
                    (line[i - 2] == " " or line[i + 1] == " "):
                errors.append([(self.line_counter, i), Const.OPERATORS])
        if len(errors) != 0:
            return errors
        return None

    def _check_colon(self, line):
        """
            Проверка на пробел перед знаком ":"
        """
        index = line.find(":")
        if index != -1:
            if line[index - 1] == " ":
                return [(self.line_counter, index), Const.COLON]
        return None

    def _check_comma(self, line):
        """
            Проверка на пробел после знака ", "
        """
        errors = []
        op = line.find("\"")
        while op != -1:
            cl = line.find("\"", op + 1, len(line))
            if cl != -1:
                line = line.replace(line[op: cl + 1], "")
                op = line.find("\"")
            else:
                break
        index = line.find(",")
        while index != -1:
            if index != len(line) - 1 and line[index + 1] != " " and\
                    line[index + 1] != "\n":
                errors.append([(self.line_counter, index), Const.COMMA])
            index = line.find(",", index + 1, len(line))
        if len(errors) != 0:
            return errors
        return None

    def check_last_line(self, line):
        """
            Прверяет есть ли в конце файла одна пустая строка
        """
        if not line.endswith("\n"):
            return [(self.line_counter, 1), Const.LAST_LINE]
        return None

    def check_blank_line(self):
        """
            Прверяет есть ли в конце файла более одной пустой строки
        """
        if self.blank_lines_counter > 0:
            return [(self.line_counter, 1), Const.BLANK_LINE]
        return None
