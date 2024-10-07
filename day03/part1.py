from __future__ import annotations

import argparse
import os.path

import pytest

import support
from support import Direction4

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

DIRS = {
    '^': Direction4.UP,
    'v': Direction4.DOWN,
    '<': Direction4.LEFT,
    '>': Direction4.RIGHT,
}


def compute(s: str) -> int:
    pos = (0, 0)
    seen = {pos}
    for c in s.strip():
        pos = DIRS[c].apply(*pos)
        seen.add(pos)
    return len(seen)


INPUT_S = '''\
^>v<
'''
EXPECTED = 4


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
