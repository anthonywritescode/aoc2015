from __future__ import annotations

import argparse
import os.path
from typing import NamedTuple
from typing import Self

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

input2 = '''\
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
'''


class Item(NamedTuple):
    name: str
    n: int

    @classmethod
    def parse(cls, s: str) -> Self:
        name, n_s = s.split(': ')
        return cls(name, int(n_s))


def compute(s: str) -> int:
    sieve = dict(Item.parse(s) for s in input2.splitlines())

    for i, line in enumerate(s.splitlines(), 1):
        _, rest = line.split(': ', 1)
        for s in rest.split(', '):
            item = Item.parse(s)
            if item.name in {'trees', 'cats'}:
                if item.n <= sieve[item.name]:
                    break
            elif item.name in {'pomeranians', 'goldfish'}:
                if item.n >= sieve[item.name]:
                    break
            elif sieve[item.name] != item.n:
                break
        else:
            return i

    raise AssertionError('unreachable')


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
