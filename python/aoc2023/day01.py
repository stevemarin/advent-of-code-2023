import string
from os.path import join

from aoc2023 import DATA_DIR


def read_data(filename: str) -> list[str]:
    with open(join(DATA_DIR, filename)) as fh:
        return fh.read().split("\n")


def part1(filename: str) -> int:
    data = read_data(filename)

    digits = []
    for line in data:
        if line == "":
            continue

        current_digits = "".join([c if c in string.digits else "" for c in line])
        digits.append(int(f"{current_digits[0]}{current_digits[-1]}"))

    return sum(digits)


def part2(filename) -> int:
    data = read_data(filename)

    digits = []
    for line in data:
        if line == "":
            continue

        current_digits = []
        current_length = len(line)

        for idx, c in enumerate(line):
            if c in string.digits:
                current_digits.append(int(c))
            elif c == "o":
                if idx + 3 <= current_length and line[idx : idx + 3] == "one":
                    current_digits.append(1)
            elif c == "t":
                if idx + 3 <= current_length and line[idx : idx + 3] == "two":
                    current_digits.append(2)
                elif idx + 5 <= current_length and line[idx : idx + 5] == "three":
                    current_digits.append(3)
            elif c == "f":
                if idx + 4 <= current_length and line[idx : idx + 4] == "four":
                    current_digits.append(4)
                elif idx + 4 <= current_length and line[idx : idx + 4] == "five":
                    current_digits.append(5)
            elif c == "s":
                if idx + 3 <= current_length and line[idx : idx + 3] == "six":
                    current_digits.append(6)
                elif idx + 5 <= current_length and line[idx : idx + 5] == "seven":
                    current_digits.append(7)
            elif c == "e":
                if idx + 5 <= current_length and line[idx : idx + 5] == "eight":
                    current_digits.append(8)
            elif c == "n":
                if idx + 4 <= current_length and line[idx : idx + 4] == "nine":
                    current_digits.append(9)

        digits.append(int(f"{current_digits[0]}{current_digits[-1]}"))

    return sum(digits)


if __name__ == "__main__":
    assert part1("day01_part1_sample.txt") == 142
    assert part1("day01.txt") == 54968

    assert part2("day01_part2_sample.txt") == 281
    assert part2("day01.txt") == 54094
