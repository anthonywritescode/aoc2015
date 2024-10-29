from __future__ import annotations

import argparse
import itertools
import os.path
from collections.abc import Generator

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _factors(n: int) -> Generator[int]:
    max_n = int(n ** .5)

    i = 1
    while i <= max_n:
        if n % i == 0:
            yield i
            yield n // i

        i += 1


def compute(s: str) -> int:
    target = int(s)

    for n in itertools.count(1):
        if sum(set(_factors(n))) * 10 > target:
            return n

    raise AssertionError('unreachable')


INPUT_S = '''\
130
'''
EXPECTED = 8


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
