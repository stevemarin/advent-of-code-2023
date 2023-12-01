from math import lcm
from os.path import join

from aoc2023 import DATA_DIR


def read_input(filename: str) -> tuple[list[str], dict[str, str]]:
    with open(join(DATA_DIR, filename), "r") as fh:
        content = fh.read().strip()

    turns, nodes = content.split("\n\n")
    nodes_tmp: dict[str, str] = {}

    for node in nodes.split("\n"):
        name, left_right = node.split("=")
        left, right = left_right.strip()[1:-1].split(",")

        assert name + "_L" not in nodes_tmp
        assert name + "_R" not in nodes_tmp

        name = name.strip()
        nodes_tmp[name + "_L"] = left.strip()
        nodes_tmp[name + "_R"] = right.strip()

    return list(turns), nodes_tmp


def part1(filename: str) -> int:
    # super simple, just walk following the directions
    # until we hit the end
    turns, nodes = read_input(filename)

    idx, name = 0, "AAA"
    while True:
        # the modulo (%) is because if you hit the end of the
        # directions, you start over
        turn = turns[idx % len(turns)]
        name = nodes[name + "_" + turn]

        idx += 1

        if name == "ZZZ":
            return idx


def part2(filename: str) -> int:
    # the trick here is each starting point hits a single ending point
    # with a fixed frequency. just need to calculate when those
    # frequencies align, which is the least common multiple
    turns, nodes = read_input(filename)

    starting_nodes = set(
        map(lambda x: x[:-2], filter(lambda x: x[-3] == "A", list(nodes.keys())))
    )

    cycle_legths: list[int] = []

    for name in starting_nodes:
        idx, num_z = 0, 0
        z_count: dict[str, list[int]] = {}
        while True:
            # set this to ~15 during testing, but set lower not to run
            # faster while minimally keeping the checks
            if num_z == 3:
                # make sure each start locations corresponds to exactly
                # one end location
                assert len(z_count) == 1
                z_diffs = [
                    value[i + 1] - value[i]
                    for value in z_count.values()
                    for i in range(len(value) - 1)
                ]
                # check consistency of cycle lengths
                # they appear to have same legnth with no burn-in
                assert all([z_diffs[0] == z for z in z_diffs])
                cycle_legths.append(z_diffs[0])
                break

            # walk the maze
            turn = turns[idx % len(turns)]
            name = nodes[name + "_" + turn]

            # record endpoints for asserts above
            if name[-1] == "Z":
                num_z += 1
                if name not in z_count:
                    z_count[name] = [idx]
                else:
                    z_count[name].append(idx)

            idx += 1

    return lcm(*cycle_legths)


if __name__ == "__main__":
    assert part1("day08_sample1.txt") == 2
    assert part1("day08_sample2.txt") == 6
    assert part1("day08.txt") == 19241

    assert part2("day08_sample3.txt") == 6
    assert part2("day08.txt") == 9606140307013
