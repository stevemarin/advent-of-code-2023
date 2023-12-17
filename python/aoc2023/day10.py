# in sample1, S = F
# in sample2, S = F
# in real data, S = |

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
        ".": NotImplementedError("how'd you get to a dot?"),
    }


@dataclass
class Map:
    num_rows: int
    num_cols: int
    start_location: int
    current_location: int
    map_: array
    prev: Direction
    moves: dict[str, MoveFn] = field(default_factory=populate_moves)

    def move(self) -> None:
        pipe = self.map_[self.current_location]
        print("AAA", pipe)
        self.prev, offset = self.moves[pipe](self.prev, self.num_cols)
        self.current_location += offset

        print(
            f"Moving from {self.prev} to index {self.current_location} x {pipe}, {offset}"
        )

    def do_loop(self, steps: int | None = None) -> int:
        self.move()

        counter = 1
        while self.current_location != self.start_location:
            self.move()
            counter += 1

            if steps is not None and steps == counter:
                break

        return counter


def read_data(filename: str, replacement: str) -> Map:
    with open(join(DATA_DIR, filename), "r") as fh:
        lines = [list(line.strip()) for line in fh.read().strip().split("\n")]

    assert all([len(lines[0]) == len(line) for line in lines])

    rows = len(lines)
    cols = len(lines[0])
    map_ = array("u", "".join("".join(line) for line in lines))

    print("BBB", "".join("".join(line) for line in lines))

    start_location = map_.index("S")
    map_[start_location] = replacement

    # checking the inputs, the sample data replaces S with F and
    # the real data replaces S with |, so we just pick Direction.South
    return Map(rows, cols, start_location, start_location, map_, Direction.South)


def part1(filename: str, replacement: str) -> int:
    the_map = read_data(filename, replacement)
    loop_length = the_map.do_loop()

    print("loop length", loop_length)
    return loop_length // 2


if __name__ == "__main__":
    assert part1("day10_sample1.txt", "F") == 4
    assert part1("day10_sample2.txt", "F") == 8
    assert part1("day10.txt", "|") == 6786

