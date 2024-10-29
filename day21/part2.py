from __future__ import annotations

import argparse
import itertools
import os.path
from collections.abc import Generator
from typing import NamedTuple

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Thing(NamedTuple):
    cost: int
    damage: int
    armour: int


weapons = (
    ('Dagger', Thing(8, 4, 0)),
    ('Shortsword', Thing(10, 5, 0)),
    ('Warhammer', Thing(25, 6, 0)),
    ('Longsword', Thing(40, 7, 0)),
    ('Greataxe', Thing(74, 8, 0)),
)

armours = (
    ('Leather', Thing(13, 0, 1)),
    ('Chainmail', Thing(31, 0, 2)),
    ('Splintmail', Thing(53, 0, 3)),
    ('Bandedmail', Thing(75, 0, 4)),
    ('Platemail', Thing(102, 0, 5)),
)

rings = (
    ('Damage +1', Thing(25, 1, 0)),
    ('Damage +2', Thing(50, 2, 0)),
    ('Damage +3', Thing(100, 3, 0)),
    ('Defense +1', Thing(20, 0, 1)),
    ('Defense +2', Thing(40, 0, 2)),
    ('Defense +3', Thing(80, 0, 3)),
)


class Character(NamedTuple):
    hp: int
    damage: int
    armour: int


def _simulate(player: Character, boss: Character) -> bool:
    player_dmg = player.damage - boss.armour
    if player_dmg <= 0:
        return False

    player_turns, rem = divmod(boss.hp, player_dmg)
    player_turns += bool(rem)

    boss_dmg = boss.damage - player.armour
    if boss_dmg <= 0:
        return True

    boss_turns, rem = divmod(player.hp, boss_dmg)
    boss_turns += bool(rem)

    return player_turns <= boss_turns


def _things(
        of_class: tuple[tuple[str, Thing], ...],
) -> Generator[tuple[Thing, ...]]:
    no_names = [thing for _, thing in of_class]
    for i in range(len(of_class)):
        yield from itertools.combinations(no_names, i)


def compute(s: str) -> int:
    hp_s, damage_s, armour_s = (line.split()[-1] for line in s.splitlines())
    boss = Character(int(hp_s), int(damage_s), int(armour_s))

    maximum = -1
    for _, weapon in weapons:
        for chosen_armour in _things(armours):
            for chosen_rings in _things(rings):
                things = (weapon, *chosen_armour, *chosen_rings)
                cost_n, damage_n, armour_n = (
                    sum(thing[i] for thing in things)
                    for i in range(3)
                )
                player = Character(100, damage_n, armour_n)
                if cost_n < maximum:
                    continue
                elif not _simulate(player, boss):
                    maximum = cost_n

    return maximum


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
