from __future__ import annotations

import argparse
import itertools
import math
import os.path
import sys

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    numbers = support.parse_numbers_split(s)
    total = sum(numbers)
    target = total // 4

    best = sys.maxsize
    for i in range(1, len(numbers)):
        for cand in itertools.combinations(numbers, i):
            if sum(cand) == target:
                best = min(math.prod(cand), best)
        if best != sys.maxsize:
            break
    return best


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
