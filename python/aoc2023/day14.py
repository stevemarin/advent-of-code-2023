from array import array
from itertools import pairwise
from os.path import join

from aoc2023 import DATA_DIR, NDArray


def read_input(filename: str) -> NDArray:
    with open(join(DATA_DIR, filename), "r") as fh:
        data = [list(line) for line in fh.read().strip().split("\n")]

    rows, cols = len(data), len(data[0])
    flat_data = [item for line in data for item in line]

    return NDArray(rows, cols, array("u", flat_data))


def tilt_col_north(arr: array) -> array:
    cube_locations = (
        [-1] + [idx for idx, item in enumerate(arr) if item == "#"] + [len(arr)]
    )

    for start, stop in pairwise(cube_locations):
        num_round = arr[start + 1 : stop].count("O")
        for idx, row in enumerate(range(start + 1, stop)):
            arr[row] = "O" if idx < num_round else "."

    return arr


def tilt_north(arr: NDArray) -> NDArray:
    cols = [tilt_col_north(col) for col in arr.itercols()]
    cols = [item for c in cols for item in c]
    data = array(arr._data.typecode, [col for cols in zip(cols) for col in cols])
    return NDArray(arr.num_cols, arr.num_rows, data).transpose()


def part1(filename: str) -> int:
    arr = read_input(filename)
    arr = tilt_north(arr)

    load = 0
    for idx, row in enumerate(arr.iterrows()):
        load += (len(row) - idx) * row.count("O")

    return load


def part2(filename: str) -> None:
    arr = read_input(filename)

    # allow for some burn-in
    for cycle in range(5000):
        for _ in ("N", "W", "S", "E"):
            arr = tilt_north(arr)
            arr = arr.rotate_clockwise()
        if cycle % 100 == 0:
            print(cycle)

    for cycle in range(500):
        for _ in ("N", "W", "S", "E"):
            arr = tilt_north(arr)
            arr = arr.rotate_clockwise()

        # now start printing
        load = 0
        for idx, row in enumerate(arr.iterrows()):
            load += (len(row) - idx) * row.count("O")
        print(cycle, load)

    # visually inspect output to get cycle parameters


if __name__ == "__main__":
    assert part1("day14_sample.txt") == 136
    assert part1("day14.txt") == 112046

    # inspection used to get cycle parameters
    # part2("day14_sample.txt")

    desired_cycle_count = 1000000000
    cycle = [69, 69, 65, 64, 65, 63, 68]
    cycle_burn_in = 3
    assert cycle[(desired_cycle_count - cycle_burn_in) % len(cycle)] == 64

    # inspection used to get cycle parameters
    # part2("day14.txt")

    cycle_burn_in = 5000 + 22
    cycle = [
        104651,
        104625,
        104620,
        104626,
        104646,
        104642,
        104633,
        104644,
        104632,
        104627,
        104619,
        104639,
        104649,
        104640,
        104637,
        104625,
        104634,
        104626,
        104632,
        104642,
        104647,
        104644,
        104618,
        104627,
        104633,
        104639,
        104635,
        104640,
    ]

    assert cycle[(desired_cycle_count - cycle_burn_in) % len(cycle)] == 104619
