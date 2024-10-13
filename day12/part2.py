from __future__ import annotations

import argparse
import json
import os.path
from typing import TypeAlias

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


_Data: TypeAlias = dict[str, '_Data'] | list['_Data'] | str | int


def _helper(data: _Data) -> int:
    if isinstance(data, int):
        return data
    elif isinstance(data, str):
        return 0
    elif isinstance(data, list):
        return sum(_helper(v) for v in data)
    elif isinstance(data, dict):
        if any(v == 'red' for v in data.values()):
            return 0
        else:
            return sum(_helper(v) for v in data.values())
    else:
        raise AssertionError('unreachable!')


def compute(s: str) -> int:
    parsed = json.loads(s)
    return _helper(parsed)


INPUT_S = '''\
[1,{"c":"red","b":2},3]
'''
EXPECTED = 4


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
        ('{"a":[-1,1]}', 0),
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
