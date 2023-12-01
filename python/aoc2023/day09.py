from itertools import pairwise
from os.path import join

from aoc2023 import DATA_DIR


def read_data(fileame: str) -> list[list[int]]:
    lines: list[list[int]] = []
    with open(join(DATA_DIR, fileame), "r") as fh:
        for line in fh.read().strip().split("\n"):
            lines.append(list(map(int, line.split())))

    return lines


def part1(filename: str) -> int:
    lines = read_data(filename)

    sum_ = 0
    for line in lines:
        line_diffs = [line]

        while not set(line_diffs[-1]) == {0}:
            line_diff = line_diffs[-1]
            next_line_diff = [
                line_diff[i + 1] - line_diff[i] for i in range(len(line_diff) - 1)
            ]
            line_diffs.append(next_line_diff)

        for prev, current in pairwise(reversed(line_diffs)):
            current.append(current[-1] + prev[-1])

        sum_ += line_diffs[0][-1]

    return sum_


def part2(filename: str) -> int:
    lines = read_data(filename)

    sum_ = 0
    for line in lines:
        line_diffs = [line]

        while not set(line_diffs[-1]) == {0}:
            line_diff = line_diffs[-1]
            next_line_diff = [
                line_diff[i + 1] - line_diff[i] for i in range(len(line_diff) - 1)
            ]
            line_diffs.append(next_line_diff)

        for prev, current in pairwise(reversed(line_diffs)):
            current.insert(0, current[0] - prev[0])

        sum_ += line_diffs[0][0]

    return sum_


if __name__ == "__main__":
    assert part1("day09_sample.txt") == 114
    assert part1("day09.txt") == 1953784198

    assert part2("day09_sample.txt") == 2
    assert part2("day09.txt") == 957
