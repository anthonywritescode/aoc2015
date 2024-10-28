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


def compute(s: str) -> int:
    rules, molecule = s.strip().split('\n\n')

    seen: set[str] = set()
    for rule in rules.splitlines():
        src, dest = rule.split(' => ')
        seen.update(_possible(molecule, src, dest))

    return len(seen)


INPUT_S = '''\
H => HO
H => OH
O => HH

HOHOHO
'''
EXPECTED = 7


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
