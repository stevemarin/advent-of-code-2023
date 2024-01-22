from dataclasses import dataclass
from itertools import batched
from os.path import join

from aoc2023 import DATA_DIR, Range

Shifted = Range | None
Unshifted = Range | None


@dataclass
class RangeMap:
    source: Range
    dest: Range

    def __post_init__(self):
        assert len(self.source) == len(self.dest)
        self.diff = self.dest.start - self.source.start

    def shift(self, range_: Range) -> tuple[Shifted, Unshifted]:
        intersection = self.source.intersection(range_)

        # no intersection
        if intersection is None:
            return None, range_
        # complete intersection
        elif intersection == range_:
            return range_.shift_by(self.diff), None
        # partial intersection
        else:
            shifted = intersection.shift_by(self.diff)
            unshifted = range_ - intersection

            assert unshifted is not None
            assert len(unshifted) <= 2
            assert len(unshifted) >= 1

            return shifted, unshifted[0]


Layer = list[RangeMap]


@dataclass
class Almanac:
    seeds: list[Range]
    layers: list[Layer]

    def __post_init__(self) -> None:
        self.locations: list[Range] = self.apply()

    @staticmethod
    def apply_layer_to_seed_range(layer: Layer, seeds: Range) -> list[Range]:
        unshifted: None | Range = seeds

        shifted: list[Range] = []
        for range_map in layer:
            assert unshifted is not None  # for type-checker
            shifted_, unshifted = range_map.shift(unshifted)
            if shifted_ is not None:
                shifted.append(shifted_)
            if unshifted is None:
                break
        else:
            if unshifted is not None:
                shifted.append(unshifted)

        return shifted

    def apply_layer(self, layer: Layer, seed_ranges: list[Range]) -> list[Range]:
        # apply the layer to each seed range...
        shifted = [
            self.apply_layer_to_seed_range(layer, seed_range)
            for seed_range in seed_ranges
        ]

        # ...and flatten
        return [range_ for ranges in shifted for range_ in ranges]

    def apply(self) -> list[Range]:
        locations = self.seeds
        for layer in self.layers:
            locations = self.apply_layer(layer, locations)

        return locations


def read_input(filename, part: int) -> Almanac:
    with open(join(DATA_DIR, filename), "r") as fh:
        lines = [line.strip() for line in fh.read().split("\n") if "map" not in line]

    seeds: list[Range]

    if part == 1:
        seeds = [Range(int(_), int(_)) for _ in lines[0].split(":")[1].split()]
    elif part == 2:
        seed_data = [int(_) for _ in lines[0].split(":")[1].split()]

        seeds = []
        for seed_start, num_seeds in batched(seed_data, 2):
            seeds.append(Range(seed_start, seed_start + num_seeds))
    else:
        raise ValueError("invalid part, must be 1 or 2")

    layers: list[Layer] = []
    layer: list[RangeMap] = []

    for line in lines[2:]:
        if line != "":
            dest_start, source_start, length = [int(_) for _ in line.split()]
            source_range = Range(source_start, source_start + length)
            dest_range = Range(dest_start, dest_start + length)
            layer.append(RangeMap(source_range, dest_range))
        else:
            layers.append(layer)
            layer = []

    return Almanac(seeds, layers)


def part1(filename: str) -> int:
    almanac = read_input(filename, 1)
    return min(range.start for range in almanac.locations)


def part2(filename: str) -> int:
    almanac = read_input(filename, 2)
    return min(range.start for range in almanac.locations)


assert Range(1, 3) == Range(1, 3)
assert Range(1, 4) != Range(1, 3)

assert Range(3, 4).intersection(Range(1, 2)) is None
assert Range(3, 4).intersection(Range(3, 4)) == Range(3, 4)
assert Range(3, 4).intersection(Range(3, 3)) == Range(3, 3)

assert Range(1, 2) - Range(0, 3) is None
assert Range(1, 4) - Range(6, 9) == [Range(1, 4)]
assert Range(1, 4) - Range(2, 3) == [Range(1, 2), Range(3, 4)]

if __name__ == "__main__":
    assert part1("day05_sample.txt") == 35
    assert part1("day05.txt") == 424490994

    assert part2("day05_sample.txt") == 46
    assert part2("day05.txt") == 15290096
