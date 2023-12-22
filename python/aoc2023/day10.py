from array import array
from dataclasses import dataclass, field
from enum import Enum, auto
from os.path import join
from typing import Callable

from aoc2023 import DATA_DIR


class Direction(Enum):
    North = auto()
    East = auto()
    South = auto()
    West = auto()


NumCols = int
Offset = int
MoveFn = Callable[[Direction, NumCols], tuple[Direction, Offset]]


def populate_moves():
    def move_bar(prev: Direction, num_cols: NumCols) -> tuple[Direction, Offset]:
        if prev == Direction.North:
            return Direction.North, num_cols
        else:
            return Direction.South, -num_cols

    def move_dash(prev: Direction, _: NumCols) -> tuple[Direction, Offset]:
        assert prev in (Direction.West, Direction.East)
        if prev == Direction.East:
            return Direction.East, -1
        else:
            return Direction.West, 1

    def move_L(prev: Direction, num_cols: NumCols) -> tuple[Direction, Offset]:
        assert prev in (Direction.North, Direction.East)
        if prev == Direction.North:
            return Direction.West, 1
        else:
            return Direction.South, -num_cols

    def move_J(prev: Direction, num_cols: NumCols) -> tuple[Direction, Offset]:
        assert prev in (Direction.North, Direction.West)
        if prev == Direction.North:
            return Direction.East, -1
        else:
            return Direction.South, -num_cols

    def move_7(prev: Direction, num_cols: NumCols) -> tuple[Direction, Offset]:
        assert prev in (Direction.South, Direction.West)
        if prev == Direction.South:
            return Direction.East, -1
        else:
            return Direction.North, num_cols

    def move_F(prev: Direction, num_cols: NumCols) -> tuple[Direction, Offset]:
        assert prev in (Direction.South, Direction.East)
        if prev == Direction.South:
            return Direction.West, 1
        else:
            return Direction.North, num_cols

    return {
        "|": move_bar,
        "-": move_dash,
        "L": move_L,
        "J": move_J,
        "7": move_7,
        "F": move_F,
    }


@dataclass
class Map:
    num_rows: int
    num_cols: int
    start_location: int
    current_location: int
    map_: array
    prev_dir: Direction
    moves: dict[str, MoveFn] = field(default_factory=populate_moves)

    def move(self) -> None:
        pipe = self.map_[self.current_location]
        self.prev_dir, offset = self.moves[pipe](self.prev_dir, self.num_cols)
        self.current_location += offset

    def do_loop(self) -> list[int]:
        locations: list[int] = []
        while self.current_location != self.start_location or len(locations) == 0:
            self.move()
            locations.append(self.current_location)

        return locations


def read_data(filename: str, replacement: str) -> Map:
    with open(join(DATA_DIR, filename), "r") as fh:
        lines = [list(line.strip()) for line in fh.read().strip().split("\n")]

    assert all([len(lines[0]) == len(line) for line in lines])

    rows = len(lines)
    cols = len(lines[0])
    map_ = array("u", "".join("".join(line) for line in lines))

    start_location = map_.index("S")
    map_[start_location] = replacement

    # checking the inputs, the sample data replaces S with F and
    # the real data replaces S with |, so we just pick Direction.South
    return Map(rows, cols, start_location, start_location, map_, Direction.South)


def part1(filename: str, replacement: str) -> int:
    the_map = read_data(filename, replacement)
    locations = the_map.do_loop()

    return len(locations) // 2


def shoelace(coordinates: list[int], num_cols: int) -> int:
    # given (x, y) coordinates, the shoelace formula calculates the area
    # note that this is AREA not number of interior points
    sum_ = 0
    x2, y2 = divmod(coordinates[0], num_cols)
    for p2 in coordinates[1:] + coordinates[0:1]:
        x1, y1 = x2, y2
        x2, y2 = divmod(p2, num_cols)
        sum_ += (x1 * y2) - (x2 * y1)

    int_sum = abs(sum_ // 2)

    assert int_sum == abs(sum_ / 2)

    return int_sum


def inverse_picks(area: float, num_external_points: int) -> int:
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


def part2(filename: str, replacement: str):
    the_map = read_data(filename, replacement)
    locations = the_map.do_loop()
    area = shoelace(locations, the_map.num_cols)
    return inverse_picks(area, len(locations))


if __name__ == "__main__":
    # in sample1, S = F
    # in sample2, S = F
    # in sample2, S = F
    # in sample2, S = F
    # in sample2, S = F
    # in sample2, S = 7
    # in real data, S = |

    assert part1("day10_sample1.txt", "F") == 4
    assert part1("day10_sample2.txt", "F") == 8
    assert part1("day10.txt", "|") == 6786

    assert part2("day10_sample1.txt", "F") == 1
    assert part2("day10_sample2.txt", "F") == 1
    assert part2("day10_sample3.txt", "F") == 4
    assert part2("day10_sample4.txt", "F") == 4
    assert part2("day10_sample5.txt", "F") == 8
    assert part2("day10_sample6.txt", "7") == 10
    assert part2("day10.txt", "|") == 495
