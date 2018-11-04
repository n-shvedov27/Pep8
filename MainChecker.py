from Variables import Variables
from CheckerBasic import CheckerBasic
from CheckerBlankLines import CheckerBlankLines
from CheckerSpaces import CheckerSpaces
from CheckerBracket import CheckerBracket


class Checker:
    def __init__(self):
        self.variables = Variables()
        checkers = []
        checkers.append(CheckerBasic())
        checkers.append(CheckerBlankLines())
        checkers.append(CheckerSpaces())
        checkers.append(CheckerBracket())
        self.check_tests = []
        for checker in checkers:
            self.check_tests.extend(checker.checkers)

    def check_file(self, filelike_object):
        for line in filelike_object:
            self.check_line(line)

    def check_line(self, line):
        # В формате: [(строка, столбец), ошибка]
        self.variables.line_counter += 1
        for check in self.check_tests:
            result = check(line, self.variables)
            if result is not None:
                if type(result[0]) == tuple:
                    self.variables.result_list.append(result)
                else:
                    self.variables.result_list.extend(result)
        self.previous_line_contains_class(line)
        self.nesting_classes(line)
        self.nesting_methods(line)
        self.in_bracket(line)
        self.begining(line)
        return self.variables.result_list

    def begining(self, line):
        copy_line = line[:]
        while copy_line.startswith(' '):
            copy_line = copy_line[1:]
        if not (copy_line == '\n' or copy_line == ''):
            self.variables.begining = False

    def previous_line_contains_class(self, line):
        if "class " in line:
            self.variables.previous_line_contains_class = True
        else:
            self.variables.previous_line_contains_class = False

    def nesting_classes(self, line):
        if line.startswith(' ' * (self.variables.in_class*4)+"class"):
            self.variables.in_class += 1

    def nesting_methods(self, line):
        if line.startswith(' ' * (self.variables.in_method*4)+"def"):
            self.variables.in_method += 1

    def in_bracket(self, line):
        count_of_bracer = 0
        for char in line:
            if char == '[' or char == '(':
                count_of_bracer += 1
            if char == ']' or char == ')':
                count_of_bracer -= 1
        self.variables.in_bracket += count_of_bracer

    def print_errors(self):
        if len(self.variables.result_list) != 0:
            for error in self.variables.result_list:
                print(self.make_string_error(error))
                print()
        else:
            print("Ok")

    def make_string_error(self, error):
        res = "Line:{0}, column:{1}" + '\n' + "Error:{2}"
        return res.format(error[0][0], error[0][1], error[1])
