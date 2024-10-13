from __future__ import annotations

import argparse
import os.path
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Deer(NamedTuple):
    name: str
    speed: int
    duration: int
    rest: int


def _compute_one(deer: Deer, n: int) -> int:
    period = deer.duration + deer.rest
    rem = n % period
    if rem < deer.duration:
        # in flight!
        return (
            # previous periods
            (n // period) * deer.duration * deer.speed +
            rem * deer.speed
        )
    else:
        # resting!
        return ((n // period) + 1) * deer.duration * deer.speed


def compute(s: str, *, n: int = 2503) -> int:
    deers = []
    for line in s.splitlines():
        name, _, _, speed_s, _, _, duration_s, *_, rest_s, _ = line.split()
        deers.append(Deer(name, int(speed_s), int(duration_s), int(rest_s)))

    return max(_compute_one(deer, n=n) for deer in deers)


INPUT_S = '''\
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
'''
EXPECTED = 1120


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, n=1000) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
