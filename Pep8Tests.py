import unittest
import os

from CheckerBasic import CheckerBasic
from CheckerBlankLines import CheckerBlankLines
from CheckerBracket import CheckerBracket
from CheckerSpaces import CheckerSpaces
from Variables import Variables
from MainChecker import Checker

H = 3

ROOT_PATH = os.getcwd()


class Pep8Test(unittest.TestCase):
    def test1_check_length_good2(self):
        my_checker = CheckerBasic()
        vars = Variables()
        vars.in_class = 1
        my_checker._check_out_of_class("   ", vars)
        self.assertEquals(vars.in_class, 0)

    def test1_check_length_good3(self):
        my_checker = CheckerBasic()
        vars = Variables()
        vars.in_method = 1
        my_checker._check_out_of_method("   ", vars)
        self.assertEquals(vars.in_method, 0)

    def test1_check_length_good4(self):
        my_checker = CheckerBlankLines()
        vars = Variables()
        actual = my_checker._check_two_blank_lines("\n", vars)
        vars.begining = False
        actual = my_checker._check_two_blank_lines("  class a", vars)
        self.assertEquals(actual, [(0, 1),
                                   ' E302 expected 2 blank lines, found 1'])

    def test1_check_length_good5(self):
        my_checker = CheckerBlankLines()
        vars = Variables()
        vars.begining = False
        vars.in_class = 1
        actual = my_checker._check_two_blank_lines("  class a", vars)
        self.assertEquals(actual, [(0, 1),
                                   ' E302 expected 2 blank lines, found 0'])

    def test1_check_length_good6(self):
        my_checker = CheckerBlankLines()
        vars = Variables()
        vars.begining = False
        vars.in_class = 1
        vars.blank_lines_counter = 10
        actual = my_checker._check_two_blank_lines("  class a", vars)
        self.assertEquals(actual, [(0, 1), ' E303 too many blank lines(10)'])

    def test1_check_length_good7(self):
        my_checker = CheckerBlankLines()
        actual = my_checker._check_blank_line_after_decorator("@adwa",
                                                              Variables())
        self.assertEquals(actual, None)

    def test1_check_length_good8(self):
        my_checker = Checker()
        my_checker.begining(" w")
        self.assertEquals(my_checker.variables.begining, False)

    def test1_check_length_good9(self):
        my_checker = CheckerSpaces()
        vars = Variables()
        actual = my_checker._check_spases_around_keyword_or_equals_parameter(
            "a =2", vars)
        self.assertEquals(actual, [
            (0, 2), ' E251 unexpected spaces around keyword / parameter equals'
        ])

    def test1_check_length_good10(self):
        my_checker = CheckerSpaces()
        vars = Variables()
        actual = my_checker._check_spases_around_keyword_or_equals_parameter(
            "def a:", vars)
        self.assertEquals(actual, None)

    def test1_check_length_good11(self):
        my_checker = CheckerSpaces()
        vars = Variables()
        actual = my_checker._check_mult_four_ident(" ", vars)
        self.assertEquals(
            actual, [(0, 1), ' E111 indentation is not a multiple of four'])

    def test1_check_length_good(self):
        my_checker = CheckerBasic()
        expected = [(0, 0), ' E501 line too long(115 > 79 characters)']
        actual = my_checker._check_length(
            "a = 'wadwdawdawdawdawdawdawdawdawdawdawdwad" +
            "wdawdawdawdawdawdawdawdawdawdawdwad" +
            "wdawdawdawdawdawdawdawdawdawdawdwad' ",
            Variables())
        self.assertEqual(actual, expected)

    def test2_check_mult_import(self):
        my_checker = CheckerBasic()
        expected = [(0, 10), ' E401 multiple imports in one line']
        actual = my_checker._check_mult_import("import awd, awd", Variables())
        self.assertEqual(actual, expected)

    def test3_check_tabs(self):
        my_checker = CheckerBasic()
        expected = [(0, 0), ' W191 indentation contains tabs']
        actual = my_checker._check_tabs("\ta = 2", Variables())
        self.assertEqual(actual, expected)

    def test4_check_tabs(self):
        my_checker = CheckerBlankLines()
        expected = [(0, 1), ' W293 blank line contains whitespace']
        actual = my_checker._check_blank_lines_with_spaces("   ", Variables())
        self.assertEqual(actual, expected)

    def test5_check_tabs(self):
        my_checker = CheckerBlankLines()
        expected = None
        vars = Variables()
        vars.blank_lines_counter = 1
        actual = my_checker._check_two_blank_lines("class A:", vars)
        self.assertEqual(actual, expected)

    def test6_check_tabs(self):
        my_checker = CheckerBlankLines()
        my_checker.in_decorator = True
        expected = [(0, 1), ' E304 blank lines found after function decorator']
        actual = my_checker._check_blank_line_after_decorator("", Variables())
        self.assertEqual(actual, expected)

    def test7_check_tabs(self):
        my_checker = CheckerBracket()
        expected = [(0, 1), ' E211 whitespace before (']
        actual = my_checker._check_calling_method("a ()", Variables())
        self.assertEqual(actual, expected)

    def test8_check_tabs(self):
        my_checker = CheckerBracket()
        expected = [[(0, 2), ' E211 whitespace before [']]
        actual = my_checker._check_calling_dict("a [2]=2", Variables())
        self.assertEqual(actual, expected)

    def test9_check_tabs(self):
        my_checker = CheckerSpaces()
        expected = [(0, 3), ' W291 trailing whitespace']
        actual = my_checker._check_space_in_end("a \n", Variables())
        self.assertEqual(actual, expected)

    def test10_check_tabs(self):
        my_checker = CheckerSpaces()
        expected = [(0, 6), " E261 block comment should start with '#'"]
        actual = my_checker._check_two_spaces_before_comment("a = 2 #wd",
                                                             Variables())
        self.assertEqual(actual, expected)

    def test11_check_tabs(self):
        my_checker = CheckerSpaces()
        expected = [(0, 2),
                    ' E251 unexpected spaces around keyword / parameter equals'
                    ]
        actual = my_checker._check_spases_around_keyword_or_equals_parameter(
            "a =2", Variables())
        self.assertEqual(actual, expected)

    def test12_check_tabs(self):
        my_checker = CheckerSpaces()
        expected = [(0, 1), ' E111 indentation is not a multiple of four']
        actual = my_checker._check_mult_four_ident("   a = 2", Variables())
        self.assertEqual(actual, expected)

    def test13_check_tabs(self):
        my_checker = CheckerSpaces()
        expected = [[(0, 4), ' E211 whitespace before +']]
        actual = my_checker._check_space_around_operatr("a= 2+ 2", Variables())
        self.assertEqual(actual, expected)

    def test14_check_tabs(self):
        my_checker = CheckerSpaces()
        expected = [(0, 1), ' E112 expected an indented block']
        vars = Variables()
        vars.in_class = 1
        actual = my_checker._check_exp_unexp_ident("   a = 2 + 2", vars)
        self.assertEqual(actual, expected)

    def test15_check_tabs(self):
        my_checker = CheckerSpaces()
        expected = [[(0, 0), ' E201 whitespace after (']]
        actual = my_checker._check_space_around_bracket_and_special_chars(
            "( \n", Variables())
        self.assertEqual(actual, expected)

    def test16_check_length_good(self):
        my_checker = Checker()
        with open('for_tests.txt', encoding='utf-8') as f:
            my_checker.check_file(f)
        my_checker.print_errors()
        self.assertEquals(my_checker.variables.result_list, [])

    def test17_check_length_good(self):
        my_checker = Checker()
        my_checker.check_line('a = [ [2]]')
        self.assertEqual(my_checker.variables.result_list,
                         [[(1, 4), ' E201 whitespace after ['],
                          [(1, 4), ' E211 whitespace before ['],
                          [(1, 6), ' E211 whitespace before [']])

    def test18_check_length_good(self):
        my_checker = Checker()
        my_checker.check_line('a=[2]')
        self.assertEqual(my_checker.variables.result_list,
                         [
                             [(1, 1),
                              ' E251 unexpected spaces around ' +
                              'keyword / parameter equals']])

    def test19_check_length_good(self):
        my_checker = Checker()
        my_checker.check_line('a=2')
        self.assertEqual(my_checker.print_errors(), None)


if __name__ == '__main__':
    unittest.main()
