from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

PROP1 = re.compile(r'(..).*\1')
PROP2 = re.compile(r'(.).\1')


def compute(s: str) -> int:
    total = 0
    for line in s.splitlines():
        if PROP1.search(line) and PROP2.search(line):
            total += 1
    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('qjhvhtzxzqqjkmpb', 1),
        ('xxyxx', 1),
        ('uurcxstgmygtbstg', 0),
        ('ieodomkazucvgmuy', 0),
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
