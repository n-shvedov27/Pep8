import inspect
import re


class CheckerBracket:
    def __init__(self):
        self.expr_calling_method = re.compile(r"[^= ]+ \(")
        self.expr_calling_dict = re.compile(r"([^= ]+( )\[)")
        self.checkers = []
        for s in dir(self):
            if inspect.ismethod(getattr(self, s)) and s.startswith("_check"):
                self.checkers.append(getattr(self, s))

    def _check_calling_method(self, line, vars):
        if self.expr_calling_method.match(line) is not None:
            return [(vars.line_counter, 1), " E211 whitespace before ("]

    def _check_calling_dict(self, line, vars):
        errors = []
        for m in re.finditer("\[\[", line):
            print(m.start())
            copy_line = line[:m.start()]
            if copy_line[-1] == ' ':
                while copy_line != '':
                    if copy_line[-1] == '=':
                        break
                    if copy_line[-1] != ' ':
                        errors.append([(vars.line_counter, m.start()), " E211 whitespace before ["])
                        break
                    copy_line = copy_line[:-1]
        if len(errors) != 0:
            return errors

