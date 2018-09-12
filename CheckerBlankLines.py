import inspect


class CheckerBlankLines:
    def __init__(self):
        self.in_decorator = False
        self.checkers = []
        for s in dir(self):
            if inspect.ismethod(getattr(self, s)) and s.startswith("_check"):
                self.checkers.append(getattr(self, s))

    def _check_blank_lines_with_spaces(self, line, vars):
        """
            Проверяет, что пустые строки не содержат пробелов
        """
        blank_line = ""
        for i in range(len(line)):
            if line[i] == ' ':
                blank_line += line[i]
        if len(blank_line) == len(line) and len(blank_line) != 0:
            vars.blank_lines_counter += 1
            return [(vars.line_counter, 1), " W293 blank line contains whitespace"]
        return None

    def _check_two_blank_lines(self, line, vars):
        """
            Прверяет, что перед описанием классса или функции(вне класса) есть 2 пустые строки
        """
        if len(line) == 0 or line == "\n":
            vars.blank_lines_counter += 1
            return None
        else:
            n = vars.blank_lines_counter
            if not self.in_decorator:
                vars.blank_lines_counter = 0
        copy_line = line[:-1]
        while copy_line.startswith(' '):
            copy_line = copy_line[1:]
        if copy_line.startswith('class') or copy_line.startswith('def'):
            self.in_decorator = False
            vars.blank_lines_counter = 0
            if vars.in_class == 0:
                required_blank_line = 2
            else:
                required_blank_line = 1
            if n < required_blank_line:
                if not vars.previous_line_contains_class:
                    error_str = (" E302 expected 2 blank lines, found " + str(n))
                    return [(vars.line_counter, 1), error_str]
            elif n > required_blank_line:
                error_str = (" E303 too many blank lines(" + str(n) + ")")
                return [(vars.line_counter, 1), error_str]

    def _check_blank_line_after_decorator(self, line, vars):
        """
            Прверяет, что после декоратора нет пустых строк
        """
        if vars.dec_exp.match(line) is not None:
            self.in_decorator = True
        elif(len(line) == 0 or line == "\n") and self.in_decorator:
            self.in_decorator = False
            return [(vars.line_counter, 1), " E304 blank lines found after function decorator"]
