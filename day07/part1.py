from __future__ import annotations

import argparse
import operator
import os.path
import re
from collections.abc import Callable
from typing import NamedTuple
from typing import Self

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _computable(var: str, regs: dict[str, int]) -> bool:
    if var.isdigit():
        return True
    else:
        return var in regs


def _resolve(var: str, regs: dict[str, int]) -> int:
    if var.isdigit():
        return int(var)
    else:
        return regs[var]


_ASSIGN_PAT = re.compile(r'^([^ ]+) -> ([^ ]+)$')


class Assign(NamedTuple):
    src: str
    target: str

    @classmethod
    def parse(cls, s: str) -> Self | None:
        match = _ASSIGN_PAT.match(s)
        if match is not None:
            return cls(match[1], match[2])
        else:
            return None

    def computable(self, regs: dict[str, int]) -> bool:
        return _computable(self.src, regs)

    def compute(self, regs: dict[str, int]) -> None:
        regs[self.target] = _resolve(self.src, regs)


_ANDOR_PAT = re.compile(r'([^ ]+) (AND|OR) ([^ ]+) -> ([^ ]+)$')
_ANDOR_OPS = {'AND': operator.and_, 'OR': operator.or_}


class AndOr(NamedTuple):
    op: Callable[[int, int], int]
    src1: str
    src2: str
    target: str

    @classmethod
    def parse(cls, s: str) -> Self | None:
        match = _ANDOR_PAT.match(s)
        if match is not None:
            return cls(_ANDOR_OPS[match[2]], match[1], match[3], match[4])
        else:
            return None

    def computable(self, regs: dict[str, int]) -> bool:
        return _computable(self.src1, regs) and _computable(self.src2, regs)

    def compute(self, regs: dict[str, int]) -> None:
        regs[self.target] = self.op(
            _resolve(self.src1, regs),
            _resolve(self.src2, regs),
        )


_SHIFT_PAT = re.compile(r'^([^ ]+) (LSHIFT|RSHIFT) (\d+) -> ([^ ]+)$')
_SHIFT_OPS = {'LSHIFT': operator.lshift, 'RSHIFT': operator.rshift}


class Shift(NamedTuple):
    src: str
    op: Callable[[int, int], int]
    shift: int
    target: str

    @classmethod
    def parse(cls, s: str) -> Self | None:
        match = _SHIFT_PAT.match(s)
        if match is not None:
            return cls(match[1], _SHIFT_OPS[match[2]], int(match[3]), match[4])
        else:
            return None

    def computable(self, regs: dict[str, int]) -> bool:
        return _computable(self.src, regs)

    def compute(self, regs: dict[str, int]) -> None:
        regs[self.target] = self.op(_resolve(self.src, regs), self.shift)


_NOT_PAT = re.compile(r'^NOT ([^ ]+) -> ([^ ]+)$')


class Not(NamedTuple):
    src: str
    target: str

    @classmethod
    def parse(cls, s: str) -> Self | None:
        match = _NOT_PAT.match(s)
        if match is not None:
            return cls(match[1], match[2])
        else:
            return None

    def computable(self, regs: dict[str, int]) -> bool:
        return _computable(self.src, regs)

    def compute(self, regs: dict[str, int]) -> None:
        regs[self.target] = ~_resolve(self.src, regs)


def compute(s: str) -> int:
    instructions = []
    for line in s.splitlines():
        for cls in (Assign, AndOr, Shift, Not):
            parsed = cls.parse(line)
            if parsed is not None:
                instructions.append(parsed)
                break
        else:
            raise ValueError(line)

    regs: dict[str, int] = {}
    while instructions:
        newinst = []
        for inst in instructions:
            if inst.computable(regs):
                inst.compute(regs)
            else:
                newinst.append(inst)

        if len(newinst) == len(instructions):
            raise AssertionError(f'none modified? {len(newinst)}')
        else:
            instructions = newinst

    return regs['a']


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
