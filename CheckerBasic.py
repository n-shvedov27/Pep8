import inspect


class CheckerBasic:
    def __init__(self):
        self.checkers = []
        for s in dir(self):
            if inspect.ismethod(getattr(self, s)) and s.startswith("_check"):
                self.checkers.append(getattr(self, s))

    def _check_out_of_class(self, line, vars):
        if not line.startswith(' ' * (vars.in_class*4)) and line != '\n':
            vars.in_class -= 1

    def _check_out_of_method(self, line, vars):
        if not line.startswith(' ' * (vars.in_method*4)) and line != '\n':
            vars.in_method -= 1

    def _check_length(self, line, vars):
        if len(line) > 79:
            err_str = (" E501 line too long(" + str(len(line)) +
                       " > 79 characters)")
            return [(vars.line_counter, 0), err_str]

    def _check_mult_import(self, line, vars):
        """
            Прверяет что в файле нет мультиимпортов
        """
        if line.startswith("import") and ", " in line:
            return [(vars.line_counter, line.find(", ")),
                    " E401 multiple imports in one line"]

    def _check_tabs(self, line, vars):
        """
            Прверяет наличие табуляции
        """
        index = line.find("\t")
        if index != -1:
            return [(vars.line_counter, index),
                    " W191 indentation contains tabs"]
