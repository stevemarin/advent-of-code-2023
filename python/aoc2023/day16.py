from array import array
from copy import deepcopy
from dataclasses import dataclass
from enum import IntEnum
from os.path import join

from aoc2023 import DATA_DIR, NDArray


class Heading(IntEnum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3


@dataclass
class Location:
    idx: int
    heading: Heading


@dataclass
class Route:
    map_: NDArray[str]
    locations: list[Location]
    seen_locations: NDArray[int]

    def process_locations(self) -> None:
        while len(self.locations) > 0:
            route = self.locations.pop()
            self.process_location(route)

    def get_next_location(self, location: None | Location) -> None | Location:
        if location is None:
            return None

        row, col = self.map_.idx_to_row_col(location.idx)

        match location.heading:
            case Heading.Left:
                if col == 0:
                    return None
                else:
                    return Location(location.idx - 1, location.heading)
            case Heading.Right:
                if col == self.map_.num_cols - 1:
                    return None
                else:
                    return Location(location.idx + 1, location.heading)
            case Heading.Up:
                if row == 0:
                    return None
                else:
                    return Location(location.idx - self.map_.num_cols, location.heading)
            case Heading.Down:
                if row == self.map_.num_rows - 1:
                    return None
                else:
                    return Location(location.idx + self.map_.num_cols, location.heading)
            case _:
                raise NotImplementedError

    def move(self, location: None | Location) -> None | Location:
        next_location = self.get_next_location(location)
        if next_location is None:
            return None

        next_char: str = self.map_[next_location.idx]
        match next_char, next_location.heading:
            case ".", _:
                return next_location

            case "|", h if h in (Heading.Up, Heading.Down):
                return next_location
            case "|", h if h in (Heading.Left, Heading.Right):
                next_location.heading = Heading.Up
                self.locations.append(next_location)
                next_location = deepcopy(next_location)
                next_location.heading = Heading.Down
                return next_location

            case "-", h if h in (Heading.Left, Heading.Right):
                return next_location
            case "-", h if h in (Heading.Up, Heading.Down):
                next_location.heading = Heading.Left
                self.locations.append(next_location)
                next_location = deepcopy(next_location)
                next_location.heading = Heading.Right
                return next_location

            case "/", Heading.Up:
                next_location.heading = Heading.Right
                return next_location
            case "/", Heading.Right:
                next_location.heading = Heading.Up
                return next_location
            case "/", Heading.Down:
                next_location.heading = Heading.Left
                return next_location
            case "/", Heading.Left:
                next_location.heading = Heading.Down
                return next_location

            case "\\", Heading.Up:
                next_location.heading = Heading.Left
                return next_location
            case "\\", Heading.Right:
                next_location.heading = Heading.Down
                return next_location
            case "\\", Heading.Down:
                next_location.heading = Heading.Right
                return next_location
            case "\\", Heading.Left:
                next_location.heading = Heading.Up
                return next_location

            case _:
                raise NotImplementedError

    def process_location(self, location: None | Location) -> None:
        while location is not None:
            idx = location.idx * 4 + location.heading

            if self.seen_locations[idx] == 0:
                self.seen_locations._data[idx] = 1
            elif self.seen_locations[idx] == 1:
                break
            else:
                raise NotImplementedError

            location = self.move(location)


def read_input(filename: str, first_idx: int, first_heading: Heading) -> Route:
    with open(join(DATA_DIR, filename), "r") as fh:
        lines = fh.read().strip().split("\n")

    num_rows = len(lines)
    num_cols = len(lines[0])
    num_elements = len(lines) * len(lines[0])

    map_ = NDArray(
        num_rows, num_cols, array("u", [item for line in lines for item in line])
    )

    num_cols = 4
    seen_routes = NDArray(num_elements, 4, array("H", [0] * num_elements * num_cols))

    return Route(map_, [Location(first_idx, first_heading)], seen_routes)


def part1(filename: str, first_idx: int, first_heading: Heading) -> int:
    routes = read_input(filename, first_idx, first_heading)
    routes.process_locations()
    return sum([1 if sum(row) > 0 else 0 for row in routes.seen_locations.iterrows()])


def part2(filename: str) -> int:
    routes = read_input(filename, 0, Heading.Down)

    num_rows = routes.map_.num_rows
    num_cols = routes.map_.num_cols

    starts = (
        [Location(idx, Heading.Down) for idx in range(num_cols)]
        + [
            Location(idx, Heading.Right)
            for idx in range(0, num_cols * num_rows, num_cols)
        ]
        + [
            Location(idx, Heading.Left)
            for idx in range(num_cols - 1, num_cols * (num_rows + 0) - 1, num_cols)
        ]
        + [
            Location(idx, Heading.Up)
            for idx in range((num_rows - 1) * num_cols, (num_rows + 0) * num_cols, 1)
        ]
    )

    lengths = []
    for location in starts:
        routes = read_input(filename, location.idx, location.heading)
        routes.process_locations()
        lengths.append(
            sum([1 if sum(row) > 0 else 0 for row in routes.seen_locations.iterrows()])
        )

    return max(lengths)


if __name__ == "__main__":
    assert part1("day16_sample.txt", 0, Heading.Right) == 46
    assert part1("day16.txt", 0, Heading.Down) == 7798

    assert part2("day16_sample.txt") == 51
    assert part2("day16.txt") == 8026
