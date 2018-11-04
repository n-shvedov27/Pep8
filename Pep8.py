import argparse
from MainChecker import Checker


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('input_files', metavar='F', type=str, nargs='*',
                        help='input files')
    args = parser.parse_args()
    print(args.input_files)
    input_files = args.input_files[0]
    checker = Checker()
    with open(str(input_files), encoding='utf-8') as f:
        checker.check_file(f)
    checker.print_errors()


if __name__ == "__main__":
    main()
