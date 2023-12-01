from os.path import join

from aoc2023 import DATA_DIR


class Card:
    def __init__(
        self, card_num: int, winning_numbers: set[int], numbers: set[int]
    ) -> None:
        self.card_num = card_num
        self.winning_numbers = winning_numbers
        self.numbers = numbers
        self.num_matching = len(self.winning_numbers.intersection(self.numbers))
        self.points = 0 if self.num_matching == 0 else 1 << (self.num_matching - 1)


def read_input(filename: str) -> list[Card]:
    cards: list[Card] = []

    with open(join(DATA_DIR, filename), "r") as fh:
        for line in fh.read().strip().split("\n"):
            card, rest = line.split(":")
            left, right = rest.split("|")

            card_num = int(card.split()[1])
            winning_numbers = {int(num) for num in left.split() if num.strip() != ""}
            numbers = {int(num) for num in right.split() if num.strip() != ""}
            cards.append(Card(card_num, winning_numbers, numbers))

    return cards


def part1(filename: str) -> int:
    cards = read_input(filename)
    return sum([card.points for card in cards])


def part2(filename: str) -> int:
    cards = read_input(filename)

    num_cards = [1] * len(cards)
    for idx, card in enumerate(cards):
        for offset in range(card.num_matching):
            if idx + offset < len(cards):
                num_cards[idx + offset + 1] += num_cards[idx]

    return sum(num_cards)


if __name__ == "__main__":
    assert part1("day04_sample.txt") == 13
    assert part1("day04.txt") == 23678

    assert part2("day04_sample.txt") == 30
    assert part2("day04.txt") == 15455663
