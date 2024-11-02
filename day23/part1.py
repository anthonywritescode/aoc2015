from __future__ import annotations

import argparse
import collections
import os.path

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    instructions = [line.split() for line in s.replace(',', '').splitlines()]
    regs: dict[str, int] = collections.defaultdict(int)
    pc = 0

    while 0 <= pc < len(instructions):
        match instructions[pc]:
            case 'hlf', reg:
                regs[reg] //= 2
                pc += 1
            case 'tpl', reg:
                regs[reg] *= 3
                pc += 1
            case 'inc', reg:
                regs[reg] += 1
                pc += 1
            case 'jmp', offset_s:
                pc += int(offset_s)
            case 'jie', reg, offset_s:
                if regs[reg] % 2 == 0:
                    pc += int(offset_s)
                else:
                    pc += 1
            case 'jio', reg, offset_s:
                if regs[reg] == 1:
                    pc += int(offset_s)
                else:
                    pc += 1
            case unreachable:
                raise AssertionError(f'unreachable {unreachable}')

    return regs['b']


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
