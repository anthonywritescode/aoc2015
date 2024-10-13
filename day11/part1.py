from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _as_n(c: str) -> int:
    return ord(c) - ord('a')


def _as_c(n: int) -> str:
    return chr(ord('a') + n)


_BANNED = {_as_n(c) for c in 'iol'}


def _is_valid(password_n: list[int]) -> bool:
    if any(n in _BANNED for n in password_n):
        return False

    prev = password_n[:2]
    for n in password_n[2:]:
        if prev[0] + 2 == prev[1] + 1 == n:
            break
        prev[0], prev[1] = prev[1], n
    else:
        return False

    found_one = False
    prev_n = password_n[0]
    for n in password_n[1:]:
        if n == prev_n:
            if found_one:
                return True
            else:
                found_one = True
                prev_n = -1
        else:
            prev_n = n
    else:
        return False


def _increment(password_n: list[int]) -> None:
    idx = 1
    password_n[-idx] += 1
    while password_n[-idx] >= 26:
        password_n[-idx] = 0
        idx += 1
        password_n[-idx] += 1


def compute(s: str) -> str:
    password = s.strip()
    password_n = [_as_n(c) for c in password]

    _increment(password_n)
    while not _is_valid(password_n):
        _increment(password_n)

    return ''.join(_as_c(n) for n in password_n)


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('hijklmmn', False),
        ('abbceffg', False),
        ('abbcegjk', False),
        ('abcdffaa', True),
        ('ghjaabcc', True),
    ),
)
def test(input_s: str, expected: bool) -> None:
    assert _is_valid([_as_n(c) for c in input_s]) is expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
