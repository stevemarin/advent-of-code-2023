from collections import defaultdict
from heapq import heappop, heappush
from itertools import chain
from math import inf
from os.path import join
from typing import Iterator

from aoc2023 import DATA_DIR

Grid = list[list[int]]


def read_input(filename: str) -> list[list[int]]:
    with open(join(DATA_DIR, filename)) as fh:
        return [
            list(map(int, list(row.strip()))) for row in fh.read().strip().split("\n")
        ]


# incorporated straight_line as done here:
# https://github.com/mebeim/aoc/blob/master/2023/solutions/day17.py
#
# i was missing fact that we need to know the direction of travel
# when a node was hit... see line 107


def straight_line(
    grid: Grid,
    row: int,
    col: int,
    delta_row: int,
    delta_col: int,
    min_straight: int,
    max_straight: int,
) -> Iterator[tuple[int, int, int]]:
    weight: int = 0

    for length in range(1, max_straight + 1):
        row += delta_row
        col += delta_col

        if not (0 <= row < len(grid) and 0 <= col < len(grid[0])):
            break

        weight += grid[row][col]

        if length >= min_straight:
            yield row, col, weight


def get_neighbors(
    grid: Grid,
    row: int,
    col: int,
    vertical: bool,
    min_straight: int,
    max_straight: int,
):
    gen = chain(
        straight_line(
            grid,
            row,
            col,
            1 if vertical else 0,
            0 if vertical else 1,
            min_straight,
            max_straight,
        ),
        straight_line(
            grid,
            row,
            col,
            -1 if vertical else 0,
            0 if vertical else -1,
            min_straight,
            max_straight,
        ),
    )

    for row, col, weight in gen:
        yield (row, col, not vertical), weight


def dijkstra(
    grid: Grid,
    min_straight: int,
    max_straight: int,
) -> int:
    # make sure it's square
    assert all(len(row) == len(grid[0]) for row in grid)

    rows, cols = len(grid), len(grid[0])

    frontier = [(0, (0, 0, True)), (0, (0, 0, False))]

    costs = defaultdict(lambda: inf)
    seen = set()

    while frontier:
        cost, (row, col, vertical) = heappop(frontier)

        if (row, col) == (rows - 1, cols - 1):
            return cost

        if (row, col, vertical) in seen:
            continue

        seen.add((row, col, vertical))

        for (nrow, ncol, nvertical), weight in get_neighbors(
            grid, row, col, vertical, min_straight, max_straight
        ):
            new_cost = cost + weight

            if new_cost < costs[(nrow, ncol, nvertical)]:
                costs[(nrow, ncol, nvertical)] = new_cost
                heappush(frontier, (new_cost, (nrow, ncol, nvertical)))

    raise ValueError("didn't reach end")


def part1(filename: str) -> int:
    grid = read_input(filename)
    return dijkstra(grid, 1, 3)


def part2(filename: str) -> int:
    grid = read_input(filename)
    return dijkstra(grid, 4, 10)


if __name__ == "__main__":
    assert part1("day17_sample.txt") == 102
    assert part1("day17.txt") == 1128

    assert part2("day17_sample.txt") == 94
    assert part2("day17_sample2.txt") == 71
    assert part2("day17.txt") == 1268
