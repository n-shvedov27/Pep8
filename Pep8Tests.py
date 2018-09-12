#!/usr/bin/python3
import unittest
import os

import Const
from Checker import MainChecker

ROOT_PATH = os.getcwd()


class Pep8Test(unittest.TestCase):
    def test1_check_length_good(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_length("12")
        self.assertEqual(actual, expected)

    def test2_check_length_last_good(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_length("012345678901234567890123456789" +
                                         "12345678901234567890123456789012" +
                                         "34567890123456789")
        self.assertEqual(actual, expected)

    def test3_check_length_wrong(self):
        MyChecker = MainChecker()
        expected = [(0, 1), " E501 line too long(83 > 79 characters)"]
        actual = MyChecker._check_length("012345678901234567890123456789" +
                                         "12345678901234567890123456789012" +
                                         "345678901234567890123")
        self.assertEqual(actual, expected)

    def test4_check_space_in_end_good(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_space_in_end("qrten3 4n5")
        self.assertEqual(actual, expected)

    def test5_check_space_in_end_wrong_space(self):
        MyChecker = MainChecker()
        expected = [(0, 12), Const.SPACE_IN_END]
        actual = MyChecker._check_space_in_end("qrten3 4n5  ")
        self.assertEqual(actual, expected)

    def test6_check_space_in_end_wrong_tab(self):
        MyChecker = MainChecker()
        expected = [(0, 11), Const.SPACE_IN_END]
        actual = MyChecker._check_space_in_end("qrten3 4n5	")
        self.assertEqual(actual, expected)

    def test7_two_spaces_before_comment_no_comment(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_two_spaces_before_comment("qrn3 4n5  tyr")
        self.assertEqual(actual, expected)

    def test8_two_spaces_before_comment_good(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_two_spaces_before_comment("qrn3 4n5  #tyr")
        self.assertEqual(actual, expected)

    def test9_two_spaces_before_comment_good_more_then_two(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_two_spaces_before_comment("ten3 4n5   #tyr")
        self.assertEqual(actual, expected)

    def test10_two_spaces_before_comment_wrong_one_space(self):
        MyChecker = MainChecker()
        expected = [(0, 9), Const.TWO_SPACES_BEFORE_COMMENT]
        actual = MyChecker._check_two_spaces_before_comment("qrt3 4n5 #tyr")
        self.assertEqual(actual, expected)

    def test11_two_spaces_before_comment_wrong_no_space(self):
        MyChecker = MainChecker()
        expected = [(0, 8), Const.TWO_SPACES_BEFORE_COMMENT]
        actual = MyChecker._check_two_spaces_before_comment("qen3 4n5#tyr")
        self.assertEqual(actual, expected)

    def test12_check_space_in_brackets_before_round_wrong(self):
        MyChecker = MainChecker()
        expected = [[(0, 8), " E202 whitespace before ')'"]]
        actual = MyChecker._check_space_in_brackets("a(1,2,3 )")
        self.assertEqual(actual, expected)

    def test13_check_space_in_brackets_before_round_good(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_space_in_brackets("run(2)")
        self.assertEqual(actual, expected)

    def test14_check_space_in_brackets_before_square_wrong(self):
        MyChecker = MainChecker()
        expected = [[(0, 4), " E202 whitespace before ']'"]]
        actual = MyChecker._check_space_in_brackets("v[: ]")
        self.assertEqual(actual, expected)

    def test15_check_space_in_brackets_before_square_good(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_space_in_brackets("dict[3]")
        self.assertEqual(actual, expected)

    def test16_check_space_in_brackets_before_curly_wrong(self):
        MyChecker = MainChecker()
        expected = [[(0, 7), " E202 whitespace before '}'"]]
        actual = MyChecker._check_space_in_brackets("keys{2 }")
        self.assertEqual(actual, expected)

    def test17_check_space_in_brackets_before_curly_good(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_space_in_brackets("a{a=2,b=4}")
        self.assertEqual(actual, expected)

    def test18_check_space_in_brackets_after_round_wrong(self):
        MyChecker = MainChecker()
        expected = [[(0, 1), " E201 whitespace after '('"]]
        actual = MyChecker._check_space_in_brackets("a( 1,2,3)")
        self.assertEqual(actual, expected)

    def test19_check_space_in_brackets_after_square_wrong(self):
        MyChecker = MainChecker()
        expected = [[(0, 3), " E201 whitespace after '['"]]
        actual = MyChecker._check_space_in_brackets("rte[ 5]")
        self.assertEqual(actual, expected)

    def test20_check_space_in_brackets_after_curly_wrong(self):
        MyChecker = MainChecker()
        expected = [[(0, 1), " E201 whitespace after '{'"]]
        actual = MyChecker._check_space_in_brackets("r{ 2,6}")
        self.assertEqual(actual, expected)

    def test21_check_space_in_brackets_before_round_good_operators(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_space_in_brackets("(3 + 4) - (2 * 8)")
        self.assertEqual(actual, expected)

    def test22_check_if_good(self):
        MyChecker = MainChecker()
        expected = [(1, 20), Const.UNDER_IDENT]
        MyChecker.check_line("bla bla baa if smth(")
        actual = MyChecker.check_line("absrtebnf  fgs smth:")
        self.assertEqual(actual[0], expected)

    def test23_check_if_wrong(self):
        MyChecker = MainChecker()
        expected = [[(1, 14), Const.IF], [(1, 20), Const.UNDER_IDENT]]
        MyChecker.check_line("bla bla baa if smth(")
        actual = MyChecker.check_line("absrtebnf smth:")
        self.assertTrue(actual[0] in expected and actual[1] in expected)

    def test24_check_mult_import_good(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_mult_import("import os")
        self.assertEqual(actual, expected)

    def test25_check_mult_import_good_from(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_mult_import("from k import o, l, p")
        self.assertEqual(actual, expected)

    def test26_check_mult_import_wrong(self):
        MyChecker = MainChecker()
        expected = [(0, 9), Const.MULT_IMPORT]
        actual = MyChecker._check_mult_import("import os, sys")
        self.assertEqual(actual, expected)

    def test27_check_spases_around_keyword_good(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_spases_around_keyword("(a=5, b=6)")
        self.assertEqual(actual, expected)

    def test28_check_spases_around_keyword_wrong(self):
        MyChecker = MainChecker()
        expected = [[(0, 2), Const.SPACES_AROUND_KEYWORD]]
        actual = MyChecker._check_spases_around_keyword("(a= 5, b=6)")
        self.assertEqual(actual, expected)

    def test29_check_spases_around_keyword_wrond_two_matches(self):
        MyChecker = MainChecker()
        expected = [[(0, 2), Const.SPACES_AROUND_KEYWORD],
                    [(0, 9), Const.SPACES_AROUND_KEYWORD]]
        actual = MyChecker._check_spases_around_keyword("(a= 5, b =6) abc")
        self.assertEqual(actual, expected)

    def test30_check_tabs_good(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_tabs("(a=5, b=6)")
        self.assertEqual(actual, expected)

    def test31_check_tabs_wrong(self):
        MyChecker = MainChecker()
        expected = [(0, 5), Const.TABS]
        actual = MyChecker._check_tabs("(a=5,	b=6)")
        self.assertEqual(actual, expected)

    def test32_check_mixt_good(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_mixt("(a=5,  b=6)")
        self.assertEqual(actual, expected)

    def test33_check_mixt_wrong(self):
        MyChecker = MainChecker()
        expected = [[(0, 9), Const.MIXT]]
        actual = MyChecker._check_mixt("(a=5, b=6	  )")
        self.assertEqual(actual, expected)

    def test34_check_two_blank_lines_class_good(self):
        MyChecker = MainChecker()
        expected = []
        MyChecker.check_line("import os\n")
        MyChecker.check_line("\n")
        MyChecker.check_line("\n")
        actual = MyChecker.check_line("class A(B):\n")
        self.assertEqual(actual, expected)

    def test35_check_two_blank_lines_def_good_startswith(self):
        MyChecker = MainChecker()
        expected = []
        MyChecker.check_line("import os")
        MyChecker.check_line("")
        MyChecker.check_line("")
        actual = MyChecker.check_line("def mod(a, b):")
        self.assertEqual(actual, expected)

    def test36_check_two_blank_lines_def_good(self):
        MyChecker = MainChecker()
        expected = []
        MyChecker.check_line("import os")
        MyChecker.check_line("")
        actual = MyChecker.check_line("    def mod(a, b):")
        self.assertEqual(actual, expected)

    def test37_check_two_blank_lines_def_wrong(self):
        MyChecker = MainChecker()
        expected = [(2, 1), " E302 expected 2 blank lines, found 1"]
        MyChecker.check_line("import os")
        MyChecker.check_line("")
        actual = MyChecker.check_line("def b(c):")
        self.assertEqual(actual[0], expected)

    def test38_check_two_blank_lines_class_wrong_one_line(self):
        MyChecker = MainChecker()
        expected = [(2, 1), " E302 expected 2 blank lines, found 1"]
        MyChecker.check_line("import os")
        MyChecker.check_line("")
        actual = MyChecker.check_line("class A(B):")
        self.assertEqual(actual[0], expected)

    def test39_check_two_blank_lines_class_wrong_no_lines(self):
        MyChecker = MainChecker()
        expected = [(1, 1), " E302 expected 2 blank lines, found 0"]
        MyChecker.check_line("import os")
        actual = MyChecker.check_line("def mod(a, b):")
        self.assertEqual(actual[0], expected)

    def test40_check_operators_good(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_operators("2 + 3")
        self.assertEqual(actual, expected)

    def test41_check_operators_good(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_operators("2 + 3")
        self.assertEqual(actual, expected)

    def test42_check_operators_good_brackets(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_operators("2 + (-4 * 7)")
        self.assertEqual(actual, expected)

    def test43_check_operators_good_quotes(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_operators("2\"+\"3")
        self.assertEqual(actual, expected)

    def test44_check_operators_good_digits(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_operators("2+3")
        self.assertEqual(actual, expected)

    def test45_check_operators_wrong(self):
        MyChecker = MainChecker()
        expected = [[(0, 1), Const.OPERATORS],
                    [(0, 5), Const.OPERATORS]]
        actual = MyChecker._check_operators("a+b 2+(3 * 4)")
        self.assertEqual(actual, expected)

    def test46_check_last_line_good(self):
        MyChecker = MainChecker()
        expected = []
        filename = os.path.join(ROOT_PATH, "TestFileGood.py")
        with open(filename, 'r') as f:
            MyChecker.check_file(f, filename)
            actual = MyChecker.get_errors(filename)
        self.assertEqual(actual, expected)

    def test47_check_last_line_wrong(self):
        MyChecker = MainChecker()
        expected = [[(11, 1), Const.LAST_LINE]]
        filename = os.path.join(ROOT_PATH, "TestFileWrong.py")
        with open(filename, 'r') as f:
            MyChecker.check_file(f, filename)
            actual = MyChecker.get_errors(filename)
        self.assertEqual(actual, expected)
    
    def test48_check_colon_good(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_colon("for i in a:")
        self.assertEqual(actual, expected)

    def test49_check_colon_wrong(self):
        MyChecker = MainChecker()
        expected = [(0, 11), Const.COLON]
        actual = MyChecker._check_colon("for i in a :")
        self.assertEqual(actual, expected)

    def test50_check_comma_wrong(self):
        MyChecker = MainChecker()
        expected = [(0, 3), Const.COMMA]
        actual = MyChecker._check_comma("for,rel")
        self.assertEqual(actual[0], expected)

    def test51_check_comma_good(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_comma("for, rel")
        self.assertEqual(actual, expected)

    def test52_check_oper_mult_b(self):
        MyChecker = MainChecker()
        expected = [(0, 3), Const.OPER_MULT_B]
        actual = MyChecker._check_operators("2  + 3")
        self.assertEqual(actual[0], expected)

    def test53_check_oper_mult_a(self):
        MyChecker = MainChecker()
        expected = [(0, 2), Const.OPER_MULT_A]
        actual = MyChecker._check_operators("2 +  3")
        self.assertEqual(actual[0], expected)

    def test54_check_oper_tab_b(self):
        MyChecker = MainChecker()
        expected = [(0, 2), Const.OPER_TAB_B]
        actual = MyChecker._check_operators("2\t+ 3")
        self.assertEqual(actual[1], expected)

    def test55_check_oper_tab_a(self):
        MyChecker = MainChecker()
        expected = [(0, 2), Const.OPER_TAB_A]
        actual = MyChecker._check_operators("2 +\t3")
        self.assertEqual(actual[1], expected)

    def test56_check_blank_line_after_decorator(self):
        MyChecker = MainChecker()
        expected = [(1, 1), Const.BLANK_LINE_DECORATOR]
        MyChecker.check_line("@dec\n")
        MyChecker.check_line("\n")
        actual = MyChecker.check_line("abn")
        self.assertEqual(actual[0], expected)

    def test57_check_blank_line_with_spaces_wrong(self):
        MyChecker = MainChecker()
        expected = [(0, 1), Const.BLANK_LINE_WITH_WHITESPACE]
        actual = MyChecker._check_blank_lines_with_spaces("    \n")
        self.assertEqual(actual, expected)

    def test58_check_blank_line_with_spaces_good(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_blank_lines_with_spaces("\n")
        self.assertEqual(actual, expected)

    def test59_check_mult_four_ident_good(self):
        MyChecker = MainChecker()
        expected = None
        actual = MyChecker._check_mult_four_ident("        ty")
        self.assertEqual(actual, expected)

    def test60_check_mult_four_ident_wrong(self):
        MyChecker = MainChecker()
        expected = [(0, 1), Const.MULT_FOUR_IDENT]
        actual = MyChecker._check_mult_four_ident("  ty\n")
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
