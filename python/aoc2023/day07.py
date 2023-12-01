from collections import Counter
from dataclasses import dataclass
from enum import StrEnum
from os.path import join

from aoc2023 import DATA_DIR


class HandType(StrEnum):
    Undefined = "_"
    HighCard = "A"
    OnePair = "B"
    TwoPair = "C"
    Three = "D"
    FullHouse = "E"
    Four = "F"
    Five = "G"


@dataclass
class Hand:
    cards: str
    wager: int
    hand_type: HandType = HandType.Undefined
    score: str = ""

    def __post_init__(self):
        self.hand_type = self.get_hand_type()
        self.score = (
            str(self.hand_type)
            + "-"
            + self.cards.replace("T", "V")
            .replace("J", "W")
            .replace("Q", "X")
            .replace("K", "Y")
            .replace("A", "Z")
        )

    def get_hand_type(self) -> HandType:
        counts = sorted(Counter(self.cards).values(), reverse=True)
        match counts:
            case x if x[0] == 5:
                return HandType.Five
            case x if x[0] == 4:
                return HandType.Four
            case x if x[0] == 3:
                if x[1] == 2:
                    return HandType.FullHouse
                else:
                    return HandType.Three
            case x if x[0] == 2:
                if x[1] == 2:
                    return HandType.TwoPair
                else:
                    return HandType.OnePair
            case _:
                return HandType.HighCard

    def __lt__(self, other: "Hand") -> bool:
        if not self.hand_type == other.hand_type:
            return self.hand_type < other.hand_type
        else:
            return self.score < other.score


def read_input(filename: str) -> list[Hand]:
    with open(join(DATA_DIR, filename), "r") as fh:
        values = [line.split() for line in fh.read().strip().split("\n")]
    return [Hand(cards, int(wager)) for cards, wager in values]


def part1(filename: str) -> int:
    cards = read_input(filename)

    sum_ = 0
    for idx, hand in enumerate(sorted(cards), start=1):
        sum_ += hand.wager * idx

    return sum_


@dataclass
class WildHand:
    cards: str
    wager: int
    hand_type: HandType = HandType.Undefined
    score: str = ""

    def __post_init__(self):
        self.hand_type = self.get_hand_type()
        self.score = str(self.hand_type) + self.cards.replace("T", "V").replace(
            "J", "1"
        ).replace("Q", "X").replace("K", "Y").replace("A", "Z")

    def get_hand_type(self) -> HandType:
        counter = Counter(self.cards)

        if "J" in counter:
            num_j = counter["J"]
            del counter["J"]
        else:
            num_j = 0

        assert num_j + sum(counter.values()) == 5

        counts = sorted(counter.values(), reverse=True)

        try:
            c0 = counts[0]
        except IndexError:
            c0 = 0

        try:
            c1 = counts[1]
        except IndexError:
            c1 = 0

        match c0, c1, num_j:
            case 0, 0, 5:
                return HandType.Five
            case 5, 0, 0:
                return HandType.Five
            case 4, 0, 1:
                return HandType.Five
            case 4, 1, 0:
                return HandType.Four
            case 3, 0, 2:
                return HandType.Five
            case 3, 1, 1:
                return HandType.Four
            case 3, 2, 0:
                return HandType.FullHouse
            case 3, 1, 0:
                return HandType.Three
            case 2, 0, 3:
                return HandType.Five
            case 2, 1, 2:
                return HandType.Four
            case 2, 1, 1:
                return HandType.Three
            case 2, 2, 1:
                return HandType.FullHouse
            case 2, 2, 0:
                return HandType.TwoPair
            case 2, 1, 0:
                return HandType.OnePair
            case 1, 0, 4:
                return HandType.Five
            case 1, 1, 3:
                return HandType.Four
            case 1, 1, 2:
                return HandType.Three
            case 1, 1, 1:
                return HandType.OnePair
            case 1, 1, 0:
                return HandType.HighCard
            case _:
                raise NotImplementedError(1)

    def __lt__(self, other: "WildHand") -> bool:
        if not self.hand_type == other.hand_type:
            return self.hand_type < other.hand_type
        else:
            return self.score < other.score


def read_wild_input(filename: str) -> list[WildHand]:
    with open(join(DATA_DIR, filename), "r") as fh:
        values = [line.split() for line in fh.read().strip().split("\n")]
    return [WildHand(cards, int(wager)) for cards, wager in values]


def part2(filename: str) -> int:
    hands = sorted(read_wild_input(filename))

    sum_ = 0
    for idx, hand in enumerate(hands, start=1):
        sum_ += hand.wager * idx

    return sum_


if __name__ == "__main__":
    assert part1("day07_sample.txt") == 6440
    assert part1("day07.txt") == 251029473

    assert part2("day07_sample.txt") == 5905
    assert part2("day07.txt") == 251003917
