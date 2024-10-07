from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


PAT = re.compile(r'(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)')

OPS = {
    'turn on': lambda _: 1,
    'turn off': lambda _: 0,
    'toggle': lambda x: x ^ 1,
}


def compute(s: str) -> int:
    lights = [[0] * 1000 for _ in range(1000)]
    for line in s.splitlines():
        match = PAT.fullmatch(line)
        if match is None:
            raise ValueError(line)

        op = OPS[match[1]]
        for row_n in range(int(match[2]), int(match[4]) + 1):
            for col_n in range(int(match[3]), int(match[5]) + 1):
                lights[row_n][col_n] = op(lights[row_n][col_n])

    return sum(sum(row) for row in lights)


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
