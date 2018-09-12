import re

class Variables:
    def __init__(self):
        self.previous_line_contains_class = False
        self.in_class = 0
        self.in_method = 0
        self.in_bracket = 0
        self.line_counter = 0
        self.result_list = []
        self.blank_lines_counter = 0
        self.words = re.compile(r' *(for|while|if|elif|else|def|class|try|except)')
        self.dec_exp = re.compile(r'^( )*@(.)*')




        self.ident = re.compile(r'^( )*(for|while|if|elif|else|def|class|try|except)')
        self.SPECIAL_CHARACTERS = ['-', '+', '=', '*',
                              '^', '%', '/', '!', '>', '<',
                              'd', 'r', ' ']
        self.OPERATORS = ['-', '+', '=', '*',
                          '^', '%', '/', '!', '>', '<']

