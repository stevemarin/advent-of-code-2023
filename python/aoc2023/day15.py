from os.path import join

from aoc2023 import DATA_DIR


def read_input(filename: str) -> list[str]:
    with open(join(DATA_DIR, filename), "r") as fh:
        return fh.read().strip().split(",")


def reindeer_hash(op: str) -> int:
    h = 0
    for char in op:
        h = (h + ord(char)) * 17 % 256
    return h


def part1(filename: str) -> int:
    data = read_input(filename)
    return sum([reindeer_hash(op) for op in data])


def part2(filename: str) -> int:
    data = read_input(filename)

    ops: list[tuple[str, int | None]] = []
    for op in data:
        if "-" in op:
            ops.append((op[:-1], None))
        elif "=" in op:
            ops.append((op[:-2], int(op[-1])))
        else:
            raise NotImplementedError

    box_labels: list[list[str]] = [[] for _ in range(256)]
    box_lenses: list[list[int]] = [[] for _ in range(256)]

    for label, replacement_lens in ops:
        box_idx = reindeer_hash(label)
        labels = box_labels[box_idx]
        lenses = box_lenses[box_idx]

        if replacement_lens is None:
            try:
                label_idx = labels.index(label)
                labels.pop(label_idx)
                lenses.pop(label_idx)
            except ValueError:
                continue
        else:
            try:
                label_idx = labels.index(label)
                lenses[label_idx] = replacement_lens
            except ValueError:
                labels.append(label)
                lenses.append(replacement_lens)
        
    sum_ = 0
    for box_idx, lenses in enumerate(box_lenses):
        for lens_idx, lens in enumerate(lenses):
            sum_ += (box_idx + 1) * (lens_idx + 1) * lens

    return sum_


if __name__ == "__main__":
    assert part1("day15_sample.txt") == 1320
    assert part1("day15.txt") == 494980

    assert part2("day15_sample.txt") == 145
    assert part2("day15.txt") == 247933
