import sys
import os
import argparse

from Checker import MainChecker

ROOT_PATH = os.getcwd()


def main():
    """
        Функция main разделена на логические болки:
        1. Обработка опций командной строки(о них можно прочитать в справке)
        2. Создание экземпляра класса MainChecker и обработка входных данных,
            с последующим выводом.
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('input_files', metavar='F', type=str, nargs='*',
                        help='input files')
    parser.add_argument('-e', action='store', default='utf-8',
                        help='to enter encoding table')
    parser.add_argument('-o', action='store', default=None,
                        help='to enter output file')
    args = parser.parse_args()
    encoding = args.e
    if args.o is not None:
        with open(args.o, 'w') as output_file:
            output = output_file
    else:
        output = sys.stdout
    input_files = args.input_files
    MyChecker = MainChecker()
    if not input_files:
        while True:
            line = sys.stdin.readline().rstrip('\n')
            if line == 'quit':
                break
            else:
                MyChecker.check_line(line)
    else:
        for name in input_files:
            if os.path.isfile(name):
                with open(name, 'r', encoding=encoding) as f:
                    MyChecker.check_file(f, name)
            elif os.path.isdir(name):
                for root, dirs, files in os.walk(name):
                    for filename in files:
                        if filename.endswith(".py"):
                            fullname = os.path.join(root, filename)
                            with open(fullname, 'r', encoding=encoding) as f:
                                MyChecker.check_file(f, fullname)
    MyChecker.print_errors(output)
    if output != sys.stdout:
        output_file.close()

if __name__ == "__main__":
    main()
