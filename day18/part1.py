from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str, *, steps: int = 100) -> int:
    w = len(s.splitlines()[0])
    h = len(s.splitlines())

    def _adjacent(x: int, y: int) -> int:
        return sum(
            (cx, cy) in coords
            for cx, cy in support.adjacent_8(x, y)
        )

    coords = support.parse_coords_hash(s)
    for _ in range(steps):
        new_coords = set()
        for x in range(w):
            for y in range(h):
                if (x, y) in coords and _adjacent(x, y) in {2, 3}:
                    new_coords.add((x, y))
                elif (x, y) not in coords and _adjacent(x, y) == 3:
                    new_coords.add((x, y))
        coords = new_coords

    return len(coords)


INPUT_S = '''\
.#.#.#
...##.
#....#
..#...
#.#..#
####..
'''
EXPECTED = 4


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, steps=4) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
