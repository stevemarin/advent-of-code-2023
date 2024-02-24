from array import array
from collections import deque
from copy import deepcopy
from os.path import join

from aoc2023 import DATA_DIR, NDArray


def read_input(filename: str) -> tuple[NDArray, int]:
    with open(join(DATA_DIR, filename), "r") as fh:
        rows = fh.read().strip().split()

    num_rows, num_cols = len(rows), len(rows[0])

    start_idx = -1

    arr = []
    for row_idx, row in enumerate(rows):
        for col_idx, value in enumerate(row):
            if value == "S":
                start_idx = row_idx * num_cols + col_idx
                value = "."
            arr.append(value)

    return NDArray(num_rows, num_cols, array("u", arr)), start_idx


def process_moves(grid: NDArray, start_idx: int, num_steps: int) -> int:
    """idea to use a single grid and keep grtd index came from:
    https://github.com/derailed-dash/Advent-of-Code/blob/master/src/AoC_2023/Dazbo's_Advent_of_Code_2023.ipynb
    """

    seen, reachable = set(), set()

    assert grid.num_cols == grid.num_rows
    width = grid.num_rows

    queue: deque[tuple[int, int, int, int]] = deque([(0, 0, start_idx, num_steps)])

    grids_for_steps = (num_steps // width) + 1

    while queue:
        grid_x, grid_y, idx, steps = queue.popleft()

        if steps >= 0:
            if steps % 2 == 0:
                reachable.add((grid_x, grid_y, idx))

            if steps > 0:
                row, col = grid.idx_to_row_col(idx)
                # print(steps, grid_x, grid_y, idx, row, col)

                # if steps < 40:
                #     break

                neighbors = (
                    (row - 1, col),
                    (row + 1, col),
                    (row, col - 1),
                    (row, col + 1),
                )

                for row, col in neighbors:
                    if row < 0:
                        # going up one grid cell
                        # was at top, now bottom
                        new_grid_x, new_grid_y = grid_x, grid_y - 1
                        new_row, new_col = width - 1, col
                    elif row >= width:
                        # going up one grid cell
                        # was at bottom, now top
                        new_grid_x, new_grid_y = grid_x, grid_y + 1
                        new_row, new_col = 0, col
                    elif col < 0:
                        # going left one grid cell
                        # was at left, now right
                        new_grid_x, new_grid_y = grid_x - 1, grid_y
                        new_row, new_col = row, width - 1
                    elif col >= width:
                        # going right one grid cell
                        # was at right, now left
                        new_grid_x, new_grid_y = grid_x + 1, grid_y
                        new_row, new_col = row, 0
                    else:
                        new_grid_x, new_grid_y = grid_x, grid_y
                        new_row, new_col = row, col

                    if not (0 <= new_row < width and 0 <= new_col < width):
                        raise NotImplementedError

                    new_idx = grid.row_col_to_idx(new_row, new_col)

                    if (new_grid_x, new_grid_y, new_idx) in seen or grid[
                        new_idx
                    ] == "#":
                        # print(grid_x, grid_y, idx, grid[idx])
                        continue

                    if abs(grid_x) > grids_for_steps:
                        print(
                            f"Too many x grids, expected max: {grids_for_steps}, got {grid_x}"
                        )

                    if abs(grid_y) > grids_for_steps:
                        print(
                            f"Too many y grids, expected max: {grids_for_steps}, got {grid_y}"
                        )

                    queue.append((new_grid_x, new_grid_y, new_idx, steps - 1))
                    seen.add((new_grid_x, new_grid_y, new_idx))

    return len(reachable)


def print_locations(arr: NDArray, locations: set[int]) -> None:
    arr = deepcopy(arr)

    for location in locations:
        arr._data[location] = "0"

    for row in arr.iterrows():
        print("".join(row))


def part1(filename: str, num_steps: int) -> int:
    grid, start_idx = read_input(filename)
    return process_moves(grid, start_idx, num_steps)


def part2(filename: str, num_steps: int) -> int:
    """idea to use quadratic formula also came from here:
    https://github.com/derailed-dash/Advent-of-Code/blob/master/src/AoC_2023/Dazbo's_Advent_of_Code_2023.ipynb
    """
    arr, start_idx = read_input(filename)

    half_width = arr.num_cols // 2
    width = arr.num_cols

    p_x = [half_width, half_width + width, half_width + 2 * width]
    p_y = [process_moves(arr, start_idx, x) for x in p_x]

    c = p_y[0]
    b = (4 * p_y[1] - 3 * p_y[0] - p_y[2]) / 2
    a = p_y[1] - p_y[0] - b

    x = (num_steps - width // 2) // width
    assert x == int(x)

    ans = a * x**2 + b * x + c
    assert ans == int(ans)

    return int(ans)


if __name__ == "__main__":
    assert part1("day21_sample.txt", 6) == 16
    assert part1("day21.txt", 64) == 3788

    assert part1("day21_sample.txt", 6) == 16
    assert part1("day21_sample.txt", 10) == 50
    assert part1("day21_sample.txt", 50) == 1594
    assert part1("day21_sample.txt", 100) == 6536
    assert part1("day21_sample.txt", 500) == 167004
    # assert part1("day21_sample.txt", 1000) == 668697
    # assert part1("day21_sample.txt", 5000) == 16733044

    assert part2("day21.txt", 26501365) == 631357596621921
