from __future__ import annotations

import argparse
import math
import os.path
from collections.abc import Generator
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Ingredient(NamedTuple):
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


def _allocations(total: int, n: int) -> Generator[tuple[int, ...]]:
    if n == 1:
        yield (total,)
    else:
        for i in range(total + 1):
            for sub in _allocations(total - i, n - 1):
                yield (i, *sub)


def _compute_one(
        ingredients: list[Ingredient],
        allocations: tuple[int, ...],
) -> int:
    capacity = durability = flavor = texture = calories = 0
    for ingredient, n in zip(ingredients, allocations):
        capacity += ingredient.capacity * n
        durability += ingredient.durability * n
        flavor += ingredient.flavor * n
        texture += ingredient.texture * n
        calories += ingredient.calories * n

    if calories == 500:
        return math.prod(
            max(n, 0) for n in (capacity, durability, flavor, texture)
        )
    else:
        return 0


def compute(s: str) -> int:
    ingredients = []
    for line in s.splitlines():
        name, rest = line.split(':')
        params = [int(part.split()[1]) for part in rest.split(', ')]
        ingredients.append(Ingredient(name, *params))

    return max(
        _compute_one(ingredients, allocation)
        for allocation in _allocations(100, len(ingredients))
    )


INPUT_S = '''\
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
'''
EXPECTED = 57600000


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
