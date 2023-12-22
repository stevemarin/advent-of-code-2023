from array import array
from collections.abc import Iterator
from dataclasses import dataclass
from itertools import accumulate
from os.path import join

from aoc2023 import DATA_DIR


@dataclass
class Map:
    num_rows: int
    num_cols: int
    data: array

    def iterrows(self) -> Iterator[array]:
        step = 1
        for row in range(self.num_rows):
            start = row * self.num_cols
            stop = start + self.num_cols
            yield self.data[start:stop:step]

    def itercols(self) -> Iterator[array]:
        step = self.num_cols
        for col in range(self.num_cols):
            start = col
            stop = start + self.num_cols * (self.num_rows - 1) + 1
            yield self.data[start:stop:step]

    def transpose(self) -> "Map":
        num_rows, num_cols = self.num_cols, self.num_rows
        data = array("H", [item for col in self.itercols() for item in col])
        return Map(num_rows, num_cols, data)

    def idx_to_row_col(self, idx: int) -> tuple[int, int]:
        return divmod(idx, self.num_cols)

    def row_col_to_idx(self, row: int, col: int) -> int:
        return row * self.num_cols + col


def read_data(filename: str) -> Map:
    with open(join(DATA_DIR, filename)) as fh:
        lines = [list(line) for line in fh.read().strip().split("\n")]

    num_rows = len(lines)
    num_cols = len(lines[0])
    data = [0 if item == "." else 1 for line in lines for item in line]
    acc = accumulate(data)
    mao_ = array("H", [d * a for d, a in zip(data, acc)])

    return Map(num_rows, num_cols, mao_)


def part1(filename: str, multiplier: int = 2) -> int:
    map_ = read_data(filename)

    zero_rows: list[int] = []
    for row, data in enumerate(map_.iterrows()):
        if sum(data) == 0:
            zero_rows.append(row)

    zero_cols: list[int] = []
    for col, data in enumerate(map_.itercols()):
        if sum(data) == 0:
            zero_cols.append(col)

    distances: dict[tuple[int, int], int] = {}

    num_galaxies: int = max(map_.data)
    for g1 in range(1, num_galaxies):
        idx1 = map_.data.index(g1)
        row1, col1 = map_.idx_to_row_col(idx1)
        for g2 in range(g1 + 1, num_galaxies + 1):
            idx2 = map_.data.index(g2)
            row2, col2 = map_.idx_to_row_col(idx2)

            num_extra_cols = len(
                list(filter(lambda x: min(col1, col2) < x < max(col1, col2), zero_cols))
            )
            num_extra_rows = len(
                list(filter(lambda x: min(row1, row2) < x < max(row1, row2), zero_rows))
            )

            distances[(g1, g2)] = (
                abs(row2 - row1)
                + abs(col2 - col1)
                + (multiplier - 1) * (num_extra_rows + num_extra_cols)
            )

    return sum(distances.values())


part2 = part1

if __name__ == "__main__":
    assert part1("day11_sample.txt") == 374
    assert part1("day11.txt") == 9693756

    assert part2("day11_sample.txt", 10) == 1030
    assert part2("day11_sample.txt", 100) == 8410
    assert part2("day11.txt", int(1e6)) == 717878258016
