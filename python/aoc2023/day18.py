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
    color: int


def read_input(filename: str) -> list[Step]:
    with open(join(DATA_DIR, filename)) as fh:
        lines = fh.read().strip().split("\n")

    steps: list[Step] = []
    for line in lines:
        print(line)
        direction_str, distance_str, col_str = line.split()
        steps.append(
            Step(
                Direction._value2member_map_[direction_str],  # type: ignore
                int(distance_str),
                int(col_str[2:-1], base=16),
            )
        )

    return steps


def get_extremes(steps: list[Step]) -> tuple[int, int, int, int]:
    x, y = 0, 0
    minx, maxx, miny, maxy = 0, 0, 0, 0

    for step in steps:
        match step.direction:
            case Direction.Up:
                y += step.distance
                maxy = max(y, maxy)
            case Direction.Down:
                y -= step.distance
                miny = min(y, miny)
            case Direction.Right:
                x += step.distance
                maxx = max(x, maxx)
            case Direction.Left:
                x -= step.distance
                minx = min(x, minx)

    return minx, maxx - minx, miny, maxy - miny


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
    for x2, y2 in coordinates[1:] + coordinates[0:1]:
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


if __name__ == "__main__":
    steps = read_input("day18_sample.txt")
    coords = get_coords(steps)
    shoelace_area = shoelace(coords)
    num_external_points = sum([step.distance for step in steps])
    area = inverse_picks(shoelace_area, num_external_points)
    print(shoelace_area, area, num_external_points)

    minx, xrange, miny, yrange = get_extremes(steps)
    # coords = [(x - minx, y - miny) for x, y in coords]

    for coord in coords:
        print(coord)

    grid = [["."] * 40 for _ in range(40)]
    for coord in get_coords(steps):
        grid[coord[1] + 20][coord[0] + 20] = "#"

    for row in grid:
        print("".join(row))

    for coord in coords:
        print(coord)
    print(xrange, yrange)

    # steps = read_input("day18.txt")
    # coords = get_coords(steps)
    # shoelace_area = shoelace(coords)
    # num_external_points = sum([step.distance for step in steps])
    # area = inverse_picks(shoelace_area, num_external_points)
    # print(shoelace_area, area, num_external_points)
