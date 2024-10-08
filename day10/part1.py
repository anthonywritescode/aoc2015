from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _apply(s: str) -> str:
    parts = []
    n = 0
    c = ''
    for cand in s:
        if n == 0:
            c = cand
            n = 1
        elif c != cand:
            parts.append(str(n))
            parts.append(c)
            c = cand
            n = 1
        else:
            n += 1

    parts.append(str(n))
    parts.append(c)
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
