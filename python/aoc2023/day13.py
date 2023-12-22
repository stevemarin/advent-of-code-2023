from itertools import pairwise
from os.path import join

from aoc2023 import DATA_DIR


def read_input(filename: str) -> tuple[list[list[str]], list[list[str]]]:
    with open(join(DATA_DIR, filename), "r") as fh:
        maps = [map.split() for map in fh.read().strip().split("\n\n")]

    transposed = [
        [
            "".join([map_[row][col] for row in range(len(map_))])
            for col in range(len(map_[0]))
        ]
        for map_ in maps
    ]

    return maps, transposed


def check_symmetry(map_: list[str], idx: int) -> bool:
    i: int = 0
    while idx - i >= 0 and idx + 1 + i < len(map_):
        if map_[idx - i] != map_[idx + 1 + i]:
            return False
        i += 1
    return True


def part1(filename: str) -> int:
    maps, transposed = read_input(filename)

    sum_: int = 0
    for map_rows, map_cols in zip(maps, transposed):
        for row_idx, (row, next_row) in enumerate(pairwise(map_rows)):
            if row == next_row:
                if check_symmetry(map_rows, row_idx):
                    sum_ += (row_idx + 1) * 100
                    break
                        
        for col_idx, (col, next_col) in enumerate(pairwise(map_cols)):
            if col == next_col:
                if check_symmetry(map_cols, col_idx):
                    sum_ += col_idx + 1
                    break

    return sum_


def exactly_1_difference(map_: list[str], idx: int) -> bool:
    differences: int = 0

    i: int = 0
    while idx - i >= 0 and idx + 1 + i < len(map_):
        for left, right in zip(map_[idx - i], map_[idx + 1 + i]):
            if left != right:
                differences += 1
        if differences > 1:
            return False
        i += 1

    return True if differences == 1 else False


def part2(filename: str) -> int:
    maps, transposed = read_input(filename)

    sum_: int = 0
    for map_rows, map_cols in zip(maps, transposed):
        for row_idx in range(len(map_rows) - 1):
            if exactly_1_difference(map_rows, row_idx):
                sum_ += (row_idx + 1) * 100

        for col_idx in range(len(map_cols) - 1):
            if exactly_1_difference(map_cols, col_idx):
                sum_ += (col_idx + 1)

    return sum_


if __name__ == "__main__":
    assert part1("day13_sample.txt") == 405
    assert part1("day13.txt") == 31265

    assert part2("day13_sample.txt") == 400
    assert part2("day13.txt") == 39359