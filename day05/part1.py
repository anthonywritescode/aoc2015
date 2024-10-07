from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

BAD = ('ab', 'cd', 'pq', 'xy')


def compute(s: str) -> int:
    total = 0
    for line in s.splitlines():
        if any(bad in line for bad in BAD):
            continue
        for c1, c2 in zip(line, line[1:]):
            if c1 == c2:
                break
        else:
            continue
        vowels = 0
        for c in line:
            if c in 'aeiou':
                vowels += 1
        if vowels >= 3:
            total += 1
    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('ugknbfddgicrmopn', 1),
        ('aaa', 1),
        ('jchzalrnumimnmhp', 0),
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
