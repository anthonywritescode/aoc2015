from __future__ import annotations

import argparse
import os.path

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    *_, row_s, _, col_s = s.replace(',', '').replace('.', '').split()
    row, col = int(row_s) - 1, int(col_s) - 1

    prev = 20151125
    x = 0
    y = 0

    while (x, y) != (col, row):
        prev = prev * 252533 % 33554393
        if y == 0:
            y = x + 1
            x = 0
        else:
            x += 1
            y -= 1

    return prev


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
