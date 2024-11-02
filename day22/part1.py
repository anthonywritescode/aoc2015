from __future__ import annotations

import argparse
import os.path
import sys
from typing import NamedTuple
from typing import Protocol

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class State(NamedTuple):
    mana_consumed: int
    boss_hp: int
    boss_damage: int
    player_hp: int
    player_armour: int
    player_mana: int
    effects: tuple[tuple[int, Effect], ...]
    chosen: tuple[int, ...]

    def has_won(self) -> bool:
        return self.boss_hp == 0

    def has_lost(self) -> bool:
        return self.player_hp == 0


class Spell(Protocol):
    def can_cast(self, state: State) -> bool: ...
    def cast(self, state: State) -> State: ...


class Effect(Protocol):
    def end(self, state: State) -> State: ...
    def turn(self, state: State) -> State: ...


def _state_noop(state: State) -> State:
    return state


class MagicMissile:
    cost = 53

    def can_cast(self, state: State) -> bool:
        return state.player_mana >= self.cost

    def cast(self, state: State) -> State:
        return state._replace(
            player_mana=state.player_mana - self.cost,
            boss_hp=max(0, state.boss_hp - 4),
            mana_consumed=state.mana_consumed + self.cost,
            chosen=(*state.chosen, self.cost),
        )


class Drain:
    cost = 73

    def can_cast(self, state: State) -> bool:
        return state.player_mana >= self.cost

    def cast(self, state: State) -> State:
        return state._replace(
            player_mana=state.player_mana - self.cost,
            boss_hp=max(0, state.boss_hp - 2),
            player_hp=state.player_hp + 2,
            mana_consumed=state.mana_consumed + self.cost,
            chosen=(*state.chosen, self.cost),
        )


def _has_active_effect(state: State, effect: Effect) -> bool:
    return any(isinstance(cand, type(effect)) for _, cand in state.effects)


class Shield:
    cost = 113

    def can_cast(self, state: State) -> bool:
        return (
            state.player_mana >= self.cost and
            not _has_active_effect(state, self)
        )

    def cast(self, state: State) -> State:
        return state._replace(
            player_mana=state.player_mana - self.cost,
            player_armour=7,
            effects=(*state.effects, (6, self)),
            mana_consumed=state.mana_consumed + self.cost,
            chosen=(*state.chosen, self.cost),
        )

    def end(self, state: State) -> State:
        return state._replace(player_armour=0)

    turn = staticmethod(_state_noop)


class Poison:
    cost = 173

    def can_cast(self, state: State) -> bool:
        return (
            state.player_mana >= self.cost and
            not _has_active_effect(state, self)
        )

    def cast(self, state: State) -> State:
        return state._replace(
            player_mana=state.player_mana - self.cost,
            effects=(*state.effects, (6, self)),
            mana_consumed=state.mana_consumed + self.cost,
            chosen=(*state.chosen, self.cost),
        )

    end = staticmethod(_state_noop)

    def turn(self, state: State) -> State:
        return state._replace(boss_hp=max(0, state.boss_hp - 3))


class Recharge:
    cost = 229

    def can_cast(self, state: State) -> bool:
        return (
            state.player_mana >= self.cost and
            not _has_active_effect(state, self)
        )

    def cast(self, state: State) -> State:
        return state._replace(
            player_mana=state.player_mana - self.cost,
            effects=(*state.effects, (5, self)),
            mana_consumed=state.mana_consumed + self.cost,
            chosen=(*state.chosen, self.cost),
        )

    end = staticmethod(_state_noop)

    def turn(self, state: State) -> State:
        return state._replace(player_mana=state.player_mana + 101)


SPELLS: tuple[Spell, ...] = (
    MagicMissile(), Drain(), Shield(), Poison(), Recharge(),
)


def _apply_effects(state: State) -> State:
    new_effects = []
    for remaining, effect in state.effects:
        state = effect.turn(state)
        if remaining == 1:
            state = effect.end(state)
        else:
            new_effects.append((remaining - 1, effect))

    return state._replace(effects=tuple(new_effects))


def _simulate(state: State, *spells: Spell) -> None:
    for i, spell in enumerate(spells):
        print(f'player turn {i}')
        state = _apply_effects(state)
        if state.has_won():
            print(state)
            print('won!')
            return
        print(f'cast {type(spell).__name__}')
        state = spell.cast(state)
        print(state)

        print(f'boss turn {i}')
        state = _apply_effects(state)
        if state.has_won():
            print(state)
            print('won!')
            return

        state = state._replace(
            player_hp=max(
                0,
                state.player_hp -
                max(1, state.boss_damage - state.player_armour),
            ),
        )
        if state.has_lost():
            print(state)
            print('lost!')
            return

        print(state)


def compute(s: str) -> int:
    l1, l2 = s.splitlines()
    _, _, hp_s = l1.split()
    _, damage_s = l2.split()
    hp, damage = int(hp_s), int(damage_s)

    initial = State(
        mana_consumed=0,
        boss_hp=hp,
        boss_damage=damage,
        player_hp=50,
        player_armour=0,
        player_mana=500,
        effects=(),
        chosen=(),
    )

    best = sys.maxsize
    todo = [initial]
    while todo:
        state = todo.pop()

        if state.mana_consumed >= best:
            continue

        # player turn
        state = _apply_effects(state)

        if state.has_won():
            best = min(state.mana_consumed, best)
            continue

        possible = [
            spell.cast(state) for spell in SPELLS if spell.can_cast(state)
        ]

        for cand in possible:
            if cand.has_won():
                best = min(cand.mana_consumed, best)
                possible.remove(cand)

        # boss turn
        possible = [_apply_effects(cand) for cand in possible]

        for cand in possible:
            if cand.has_won():
                best = min(cand.mana_consumed, best)
                possible.remove(cand)

        possible = [
            cand._replace(
                player_hp=max(
                    0,
                    cand.player_hp -
                    max(1, cand.boss_damage - cand.player_armour),
                ),
            )
            for cand in possible
        ]

        possible = [cand for cand in possible if not cand.has_lost()]

        todo.extend(possible)

    return best


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
