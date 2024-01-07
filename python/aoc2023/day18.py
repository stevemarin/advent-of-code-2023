from dataclasses import dataclass
from enum import StrEnum
from os.path import join

from aoc2023 import DATA_DIR


class Direction(StrEnum):
    Up = "U"
    Down = "D"
    Left = "L"
    Right = "R"


@dataclass
class Step:
    direction: Direction
    distance: int
    color: str


def read_input(filename: str) -> list[Step]:
    with open(join(DATA_DIR, filename)) as fh:
        lines = fh.read().strip().split("\n")

    steps: list[Step] = []
    for line in lines:
        direction_str, distance_str, col_str = line.split()
        steps.append(
            Step(
                Direction._value2member_map_[direction_str],  # type: ignore
                int(distance_str),
                col_str[2:-1],
            )
        )

    return steps


def get_coords(steps: list[Step]) -> list[tuple[int, int]]:
    row, col = 0, 0

    coords: list[tuple[int, int]] = []
    for step in steps:
        match step.direction:
            case Direction.Up:
                row += step.distance
            case Direction.Down:
                row -= step.distance
            case Direction.Right:
                col += step.distance
            case Direction.Left:
                col -= step.distance
        coords.append((row, col))

    return coords


def shoelace(coordinates: list[tuple[int, int]]) -> int:
    # given (x, y) coordinates, the shoelace formula calculates the area
    # note that this is AREA not number of interior points
    sum_ = 0
    x1, y1 = coordinates[0][0], coordinates[0][1]
    for x2, y2 in coordinates[1:]:
        sum_ += (x1 * y2) - (x2 * y1)
        x1, y1 = x2, y2

    int_sum = abs(sum_ // 2)

    assert int_sum == abs(sum_ / 2)

    return int_sum


def inverse_picks(area: int, num_external_points: int) -> int:
    # pick's theorem states that the area of a simple (non-self-intersecting)
    # polygon where the x, y indices are all integers (and including all
    # integer x,y points on the boundary):
    #
    # Area = internal_points + external_points / 2 - 1
    #
    # shoeloace formula gives us the area, problem formulation makes sure
    # all boundary points have integer x, y parts, so picks just gives
    # the number of integer x, y points inside, which is the solution
    num_internal_points = area + 1 - (num_external_points / 2)
    assert num_internal_points == int(num_internal_points)
    return int(num_internal_points)


def part1(filename: str) -> int:
    steps = read_input(filename)
    coords = get_coords(steps)
    shoelace_area = shoelace(coords)
    num_external_points = sum([step.distance for step in steps])
    area = inverse_picks(shoelace_area, num_external_points)
    return area + num_external_points


def part2(filename: str) -> int:
    dirs = (Direction.Right, Direction.Down, Direction.Left, Direction.Up)
    steps = [
        Step(dirs[int(step.color[-1], base=16) % 4], int(step.color[:5], base=16), "")
        for step in read_input(filename)
    ]

    coords = get_coords(steps)
    shoelace_area = shoelace(coords)
    num_external_points = sum([step.distance for step in steps])
    area = inverse_picks(shoelace_area, num_external_points)
    return area + num_external_points


if __name__ == "__main__":
    assert part1("day18_sample.txt") == 62
    assert part1("day18.txt") == 68115

    assert part2("day18_sample.txt") == 952408144115
    assert part2("day18.txt") == 71262565063800
