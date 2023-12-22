from dataclasses import dataclass, field
from itertools import pairwise
from os.path import join

from aoc2023 import DATA_DIR

# i tried and failed to use dynamic programming to do this day. i found the repo here:
# https://github.com/JoanaBLate/advent-of-code-js/blob/main/2023/day12/solve1.js
# which is wonderful. i was trying to do the same thing, so i incorporated their work.

# from typing import Sequence
# from math import comb

# def blocks_in_all_wild(wilds: int, blocks: Sequence[int]) -> int:
#     """given wilds and a set of blocks, we can convert this to a simpler problem by:
#         1. ignoring the empty space between # symbols and subtracting the number of
#            intervals in blocks (i.e. len(blocks) - 1)
#         2. assuming each run of length > 1 has length 1 and subtracting the difference
#            from the number of wilds - for all, this is -sum(blocks) + len(blocks)
#         3. now that all blocks have length 1 and can touch, we simply have wilds choose
#            len(blocks)

#     this gives the updated number of wilds as:
#     wilds_tmp = wilds - (len(blocks) - 1) - (sum(blocks) - len(blocks))

#     returns 0 when no combinations are possible
#     """
#     wilds_tmp = wilds + 1 - sum(blocks)
#     print(wilds_tmp, len(blocks), comb(wilds_tmp, len(blocks)))
#     return comb(wilds_tmp, len(blocks))


def is_good_location(row: str, start: int, length: int) -> bool:
    stop = start + length - 1
    if stop >= len(row):
        return False
    elif start - 1 >= 0 and row[start - 1] == "#":
        return False
    elif stop + 1 < len(row) and row[stop + 1] == "#":
        return False
    elif "." in row[start : stop + 1]:
        return False
    else:
        return True


@dataclass
class Block:
    length: int
    positions: list[int] = field(default_factory=list)
    paths: dict[int, int] = field(default_factory=dict)

    def leftmost_position(self, row: str, base: int) -> int | None:
        for idx in range(base, len(row)):
            if is_good_location(row, idx, self.length):
                self.positions.append(idx)
                return idx

        return None

    def rightmost_position(self, row: str, base: int) -> int | None:
        for idx in range(base, -1, -1):
            if not is_good_location(row, idx, self.length):
                continue
            elif idx in self.positions:
                return idx
            else:
                self.positions.append(idx)
                return idx

        return None

    def intermediate_positions(self, row: str) -> None:
        base = self.positions[0] + 1
        off = self.positions.pop()

        for idx in range(base, off):
            if is_good_location(row, idx, self.length):
                self.positions.append(idx)

        self.positions.append(off)

    def initialize_paths(self, first: bool):
        value = 1 if first else 0
        for position in self.positions:
            self.paths[position] = value


@dataclass
class SpringRow:
    row: str
    _blocks: tuple[int, ...]
    blocks: list[Block] = field(default_factory=list)

    @staticmethod
    def simplify_row(row: str) -> str:
        # multiple dots same as one dot, so just remove extra
        while ".." in row:
            row = row.replace("..", ".")

        # leading/trailing dots don't do anything, so remove
        row = row.strip(".")

        return row

    def __post_init__(self):
        self.row = self.simplify_row(self.row)

        for block_size in self._blocks:
            self.blocks.append(Block(block_size))

    def leftmost_positions(self) -> None:
        base: int = 0
        for block in self.blocks:
            position = block.leftmost_position(self.row, base)
            if position is None:
                continue
            base = position + block.length + 1

    def rightmost_positions(self) -> None:
        base: int = len(self.row) - self.blocks[-1].length
        for block in reversed(self.blocks):
            position = block.rightmost_position(self.row, base)
            if position is None:
                continue
            base = position - 2

    def intermediate_positions(self) -> None:
        for block in self.blocks:
            block.intermediate_positions(self.row)

    def fix_first_block(self):
        try:
            idx = self.row.index("#")
        except ValueError:
            return

        first_block = self.blocks[0]
        while first_block.positions[-1] > idx:
            _ = first_block.positions.pop()

    def fix_last_block(self) -> None:
        try:
            idx = self.row.rindex("#")
        except ValueError:
            return

        last_block = self.blocks[-1]
        length = last_block.length

        while last_block.positions[0] + length - 1 < idx:
            _ = last_block.positions.pop(0)

    def initialize_paths(self) -> None:
        for idx, block in enumerate(self.blocks):
            block.initialize_paths(True if idx == 0 else False)

    def count_good(self) -> int:
        for current, next_ in pairwise(self.blocks):
            for current_position in current.positions:
                min_next_position = current_position + current.length + 1

                try:
                    max_next_posiion = self.row.index("#", min_next_position)
                except ValueError:
                    max_next_posiion = len(self.row)

                for next_position in next_.positions:
                    if min_next_position <= next_position <= max_next_posiion:
                        next_.paths[next_position] += current.paths[current_position]

        return sum(self.blocks[-1].paths.values())

    def count(self) -> int:
        self.leftmost_positions()
        self.rightmost_positions()
        self.intermediate_positions()
        self.fix_first_block()
        self.fix_last_block()
        self.initialize_paths()
        return self.count_good()


def read_input(filename: str) -> list[SpringRow]:
    with open(join(DATA_DIR, filename), "r") as fh:
        lines = [line.split(" ") for line in fh.read().strip().split("\n")]

    block_sizes = [tuple(map(int, c.split(","))) for _, c in lines]
    return [SpringRow(row, sizes) for (row, _), sizes in zip(lines, block_sizes)]


def part1(filename: str) -> int:
    spring_rows = read_input(filename)
    return sum(row.count() for row in spring_rows)


def read_input2(filename: str) -> list[SpringRow]:
    with open(join(DATA_DIR, filename), "r") as fh:
        lines = [line.split(" ") for line in fh.read().strip().split("\n")]

    block_sizes = [tuple(map(int, c.split(","))) for _, c in lines]
    return [
        SpringRow("?".join([row] * 5), sizes * 5)
        for (row, _), sizes in zip(lines, block_sizes)
    ]


def part2(filename: str) -> int:
    spring_rows = read_input2(filename)
    return sum(row.count() for row in spring_rows)


if __name__ == "__main__":
    assert part1("day12_sample.txt") == 21
    assert part1("day12.txt") == 7191

    assert part2("day12_sample.txt") == 525152
    assert part2("day12.txt") == 6512849198636
