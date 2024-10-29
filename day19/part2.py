from __future__ import annotations

import argparse
import os.path
from collections.abc import Generator

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _possible(s: str, src: str, dest: str) -> Generator[str]:
    splits = s.split(src)
    for i in range(1, len(splits)):
        yield f'{src.join(splits[:i])}{dest}{src.join(splits[i:])}'


def _parse_rule(s: str) -> tuple[str, str]:
    src, dest = s.split(' => ')
    return src, dest


def _atoms(s: str) -> int:
    return sum(c.isupper() for c in s)


def compute(s: str) -> int:
    rules_s, molecule = s.strip().split('\n\n')

    rules = [_parse_rule(s) for s in rules_s.splitlines()]
    rules.sort(key=lambda kv: -_atoms(kv[1]))

    i = 0
    while True:
        if molecule == 'e':
            return i

        for src, dest in rules:
            if dest in molecule:
                i += 1
                molecule = molecule.replace(dest, src, 1)
                break
        else:
            raise AssertionError(f'dead end! {molecule}')


INPUT_S = '''\
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO
'''
EXPECTED = 6


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
