from dataclasses import dataclass
from os.path import join

from aoc2023 import DATA_DIR


@dataclass
class Round:
    red: int
    green: int
    blue: int

    @classmethod
    def read(cls, input: str) -> "Round":
        kwargs = {"red": 0, "green": 0, "blue": 0}
        for pull in input.strip().split(","):
            num, color = pull.strip().split(" ")
            kwargs[color.strip()] = int(num)

        return Round(**kwargs)


@dataclass
class Game:
    idx: int
    rounds: list[Round]

    @classmethod
    def read(cls, input: str, max_red: int, max_green: int, max_blue: int) -> "Game":
        left, right = input.strip().split(":")
        _, idx = left.strip().split(" ")

        rounds = [Round.read(input) for input in right.split(";")]

        return Game(
            idx=int(idx),
            rounds=rounds,
        )

    def is_valid(self, max_balls: dict[str, int]) -> bool:
        for round in self.rounds:
            for color, max_value in max_balls.items():
                if getattr(round, color) > max_value:
                    return False
        return True

    def score_min_balls(self) -> int:
        red, green, blue = 0, 0, 0
        for round in self.rounds:
            red = max(red, round.red)
            green = max(green, round.green)
            blue = max(blue, round.blue)
        return red * green * blue


def read(filename: str) -> list[Game]:
    with open(join(DATA_DIR, filename), "r") as fh:
        games = [
            Game.read(line, max_red=12, max_green=13, max_blue=14)
            for line in fh.readlines()
            if line.strip() != ""
        ]
    return games


def part1(filename: str) -> int:
    games = read(filename)
    max_balls = {"red": 12, "green": 13, "blue": 14}
    return sum(game.idx for game in games if game.is_valid(max_balls))


def part2(filename: str) -> int:
    games = read(filename)
    return sum(game.score_min_balls() for game in games)


if __name__ == "__main__":
    assert part1("day02_sample.txt") == 8
    assert part1("day02.txt") == 2256

    assert part2("day02_sample.txt") == 2286
    assert part2("day02.txt") == 74229
