from __future__ import annotations

import argparse
import collections
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    weights = {}
    edges = collections.defaultdict(set)

    for line in s.splitlines():
        src, _, dest, _, weight_s = line.split()
        weight = int(weight_s)

        weights[(src, dest)] = weight
        weights[(dest, src)] = weight

        edges[src].add(dest)
        edges[dest].add(src)

    best = 0
    todo: collections.deque[tuple[tuple[str, ...], int]]
    todo = collections.deque([((k,), 0) for k in edges])
    while todo:
        path, dist = todo.popleft()
        if len(path) == len(edges):
            best = max(dist, best)
        else:
            for cand in edges[path[-1]]:
                if cand not in path:
                    todo.append((
                        (*path, cand),
                        dist + weights[path[-1], cand],
                    ))

    return best


INPUT_S = '''\
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
'''
EXPECTED = 982


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
