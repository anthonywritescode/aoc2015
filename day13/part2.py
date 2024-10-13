from __future__ import annotations

import argparse
import collections
import itertools
import os.path
import sys

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    names = set()
    vals = collections.defaultdict(int)
    for line in s.splitlines():
        src, _, gainloss, n_s, *_, dest = line.rstrip('.').split()

        n = int(n_s)
        if gainloss == 'lose':
            n *= -1

        vals[(src, dest)] = n
        names.add(src)

    names.add('me!')

    maxval = -sys.maxsize
    for lst in itertools.permutations(names):
        val = 0
        for i, name in enumerate(lst):
            val += vals[name, lst[i - 1]]
            val += vals[name, lst[(i + 1) % len(lst)]]
        maxval = max(val, maxval)
    return maxval


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
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
