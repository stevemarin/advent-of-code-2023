from dataclasses import dataclass, field
from os.path import join
from string import digits

from __init__ import DATA_DIR

DIGITS = frozenset(digits)
DIGITS_DOT = frozenset(digits + ".")


def read_input(filename) -> list[str]:
    with open(join(DATA_DIR, filename), "r") as fh:
        lines = fh.read().strip().split("\n")

    # padding so we don't need to worry about edges
    lines = ["." + line + "." for line in lines]
    empty_line = ["." * len(lines[0])]
    return empty_line + lines + empty_line


@dataclass
class Number:
    row: int
    col: int
    length: int
    value: int
    has_symbol: bool = False


def locate_numbers(lines: list[str]) -> list[Number]:
    numbers: list[Number] = []

    num_rows, num_cols = len(lines), len(lines[0])

    row = 1
    while row < num_rows - 1:
        line = lines[row]

        col = 1
        while col < num_cols - 1:
            char = line[col]
            if char in DIGITS:
                length = 0
                while col + length < num_cols and char in DIGITS:
                    length += 1
                    char = line[col + length]
                numbers.append(Number(row, col, length, int(line[col : col + length])))
                col += length
            else:
                col += 1

        row += 1

    return numbers


def update_symbol(number: Number, lines: list[str]) -> Number:
    char_sets = [
        set(row[number.col - 1 : number.col + number.length + 1])
        for row in lines[number.row - 1 : number.row + 2]
    ]

    chars = list(set().union(*char_sets) - DIGITS_DOT)

    if len(chars) > 0:
        number.has_symbol = True

    return number


def part1(filename: str) -> int:
    lines = read_input(filename)

    numbers = locate_numbers(lines)
    numbers = [update_symbol(number, lines) for number in numbers]

    return sum([number.value for number in numbers if number.has_symbol])


@dataclass
class Gear:
    row: int
    col: int
    touching: list["Number"] = field(default_factory=list)

    def touches(self, number: Number) -> bool:
        if abs(number.row - self.row) > 1:
            return False
        elif (
            min(abs(number.col - self.col), abs(number.col + number.length - self.col - 1))
            > 1
        ):
            return False
        else:
            return True

    def update(self, numbers: list[Number]) -> "Gear":
        for number in numbers:
            if self.touches(number):
                self.touching += [number]
        return self


def locate_gears(lines: list[str]) -> list[Gear]:
    gears: list[Gear] = []

    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "*":
                gears.append(Gear(row, col))

    return gears


def part2(filename: str) -> int:
    lines = read_input(filename)

    numbers = locate_numbers(lines)
    gears = locate_gears(lines)
    gears = [gear.update(numbers) for gear in gears]

    gear_ratio_sum = 0
    for gear in gears:
        if len(gear.touching) < 2:
            continue

        assert len(gear.touching) == 2

        gear_ratio = 1
        for number in gear.touching:
            gear_ratio *= number.value

        gear_ratio_sum += gear_ratio

    return gear_ratio_sum


if __name__ == "__main__":
    assert part1("day03_sample.txt") == 4361
    assert part1("day03.txt") == 537832

    assert part2("day03_sample.txt") == 467835
    assert part2("day03.txt") == 81939900
