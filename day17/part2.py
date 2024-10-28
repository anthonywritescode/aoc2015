from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str, *, total: int = 150) -> int:
    numbers = support.parse_numbers_split(s)
    success = []

    todo: list[tuple[int, int, tuple[int, ...]]] = [(0, -1, ())]
    while todo:
        n, pos, taken = todo.pop()

        pos += 1
        if pos == len(numbers):
            continue

        cand = numbers[pos]
        if n + cand == total:
            success.append((*taken, cand))
        elif n + cand < total:
            todo.append((n + cand, pos, (*taken, cand)))

        todo.append((n, pos, taken))

    minlen = min(len(path) for path in success)
    return sum(1 for path in success if len(path) == minlen)


INPUT_S = '''\
20 15 10 5 5
'''
EXPECTED = 3


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, total=25) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
