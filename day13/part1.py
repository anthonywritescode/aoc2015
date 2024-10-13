from __future__ import annotations

import argparse
import itertools
import os.path
import sys

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    names = set()
    vals = {}
    for line in s.splitlines():
        src, _, gainloss, n_s, *_, dest = line.rstrip('.').split()

        n = int(n_s)
        if gainloss == 'lose':
            n *= -1

        vals[(src, dest)] = n
        names.add(src)

    maxval = -sys.maxsize
    for lst in itertools.permutations(names):
        val = 0
        for i, name in enumerate(lst):
            val += vals[name, lst[i - 1]]
            val += vals[name, lst[(i + 1) % len(lst)]]
        maxval = max(val, maxval)
    return maxval


INPUT_S = '''\
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
'''
EXPECTED = 330


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
