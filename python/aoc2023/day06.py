from os.path import join

from aoc2023 import DATA_DIR


def read_input(filename: str) -> tuple[tuple[int, ...], ...]:
    with open(join(DATA_DIR, filename), "r") as fh:
        lines = [line.strip() for line in fh.read().split("\n") if line.strip() != ""]

    time = tuple(map(int, lines[0].split(":")[1].split()))
    distances = tuple(map(int, lines[1].split(":")[1].split()))

    return time, distances


def get_distance(total_time: int, hold_time: int | float) -> int | float:
    return hold_time * (total_time - hold_time)


def bisect(total_time: int, distance: int, diff: float = 0.5) -> int:
    # find the least hold_time such that the distance travelled > distance
    low = 0.0
    high = total_time / 2

    assert distance < get_distance(total_time, high)

    while low < high:
        midpoint = (low + high) / 2
        dist = get_distance(total_time, midpoint)
        if abs(dist - distance) < diff:
            for idx in range(int(midpoint), total_time // 2):
                if get_distance(total_time, idx) > distance:
                    return idx
        elif dist < distance:
            low = midpoint
        else:  # dist > distance:
            high = midpoint

    raise NotImplementedError(1)


def part1(filename: str) -> int:
    times, distances = read_input(filename)

    prod = 1
    for total_time, distance in zip(times, distances):
        first_winner = bisect(total_time, distance)
        if total_time % 2 == 0:
            num_winners = (2 * ((total_time // 2) - first_winner)) + 1
        else:
            num_winners = 2 * (((total_time // 2) - first_winner) + 1)

        prod *= num_winners

    return prod


def part2(total_time: int, distance: int) -> int:
    first_winner = bisect(total_time, distance)
    if total_time % 2 == 0:
        return (2 * ((total_time // 2) - first_winner)) + 1
    else:
        return 2 * (((total_time // 2) - first_winner) + 1)


if __name__ == "__main__":
    assert part1("day06_sample.txt") == 288
    assert part1("day06.txt") == 6209190

    assert part2(71530, 940200) == 71503
    assert part2(40929790, 215106415051100) == 28545089
