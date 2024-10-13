from __future__ import annotations

import argparse
import os.path
from typing import NamedTuple
from typing import Self

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Deer(NamedTuple):
    name: str
    speed: int
    duration: int
    rest: int


class State(NamedTuple):
    deer: Deer
    pos: int
    zooming: bool
    cooldown: int

    def next(self) -> Self:
        if self.cooldown:
            return self._replace(
                pos=self.pos + self.deer.speed * self.zooming,
                cooldown=self.cooldown - 1,
            )
        else:
            if self.zooming:
                cooldown = self.deer.rest
            else:
                cooldown = self.deer.duration

            return self._replace(
                zooming=not self.zooming,
                pos=self.pos + self.deer.speed * (not self.zooming),
                cooldown=cooldown - 1,
            )


def compute(s: str, *, n: int = 2503) -> int:
    deers = []
    for line in s.splitlines():
        name, _, _, speed_s, _, _, duration_s, *_, rest_s, _ = line.split()
        deers.append(Deer(name, int(speed_s), int(duration_s), int(rest_s)))

    points = {deer.name: 0 for deer in deers}
    states = [State(deer, pos=0, zooming=False, cooldown=0) for deer in deers]
    for i in range(n):
        states = [state.next() for state in states]
        best = max(states, key=lambda state: state.pos)
        for state in states:
            if state.pos == best.pos:
                points[state.deer.name] += 1

    return max(points.values())


INPUT_S = '''\
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
'''
EXPECTED = 689


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
