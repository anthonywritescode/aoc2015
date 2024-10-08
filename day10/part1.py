from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

REG = re.compile(r'^(.)(\1*)(.*)$')


def _apply(s: str) -> str:
    parts = []
    while s:
        match = REG.match(s)
        assert match is not None
        parts.append(str(len(match[2]) + 1))
        parts.append(match[1])
        s = match[3]
    return ''.join(parts)


def compute(s: str, *, n: int = 40) -> int:
    s = s.strip()
    for _ in range(n):
        s = _apply(s)
    return len(s)


INPUT_S = '''\
1
'''
EXPECTED = 6


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, n=5) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
