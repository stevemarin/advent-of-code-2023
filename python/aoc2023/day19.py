from math import prod
from os.path import join

from aoc2023 import DATA_DIR


def read_input(filename: str):
    with open(join(DATA_DIR, filename), "r") as fh:
        workflow_section, part_section = fh.read().strip().split("\n\n")

    workflows = {}
    for workflow_str in workflow_section.split("\n"):
        name, rest = workflow_str[:-1].split("{")

        steps = []
        for step in rest.split(","):
            if ":" not in step:
                steps.append((None, None, None, step))
            else:
                op_str = ">" if ">" in step else "<"
                parameter, rest = step.split(op_str)
                value, target = rest.split(":")
                steps.append((parameter, op_str, int(value), target))

        workflows[name] = steps

    parts = []
    for part_str in part_section.split("\n"):
        part = {}
        for parameter, value in zip("xmas", part_str[1:-1].split(",")):
            v = int(value[2:])
            part[parameter] = range(v, v)
        parts.append(part)

    return workflows, parts


def part1(filename: str) -> int:
    workflows, parts = read_input(filename)

    def get_final_location(
        part: dict, loc: str, workflows: dict[str, list[dict]]
    ) -> str:
        workflow = workflows[loc]

        for parameter, op, value, target in workflow:
            if op is None:
                return (
                    target
                    if target in ("A", "R")
                    else get_final_location(part, target, workflows)
                )
            elif op == "<" and part[parameter].start < value:
                return (
                    target
                    if target in ("A", "R")
                    else get_final_location(part, target, workflows)
                )
            elif op == ">" and part[parameter].start > value:
                return (
                    target
                    if target in ("A", "R")
                    else get_final_location(part, target, workflows)
                )

        raise NotImplementedError

    total = 0
    for part in parts:
        final_location = get_final_location(part, "in", workflows)
        if final_location == "A":
            total += sum(part[c].start for c in "xmas")

    return total


def score_parts(queue: list[tuple[str, dict]], workflows: dict):
    while queue:
        current_location, part = queue.pop()
        if current_location == "A":
            yield prod(len(part[c]) + 1 for c in "xmas")
        elif current_location != "R":
            for parameter, op_str, value, target in workflows[current_location]:
                match op_str:
                    case None:
                        queue.append((target, part.copy()))
                    case ">":
                        r = part[parameter]
                        part[parameter] = range(1 + max(r.start, value), r.stop)
                        queue.append((target, part.copy()))
                        part[parameter] = range(r.start, min(r.stop, value))
                    case "<":
                        r = part[parameter]
                        part[parameter] = range(r.start, min(r.stop, value) - 1)
                        queue.append((target, part.copy()))
                        part[parameter] = range(max(r.start, value), r.stop)


def part2(filename: str) -> int:
    workflows, _ = read_input(filename)

    part = {c: range(1, 4000) for c in "xmas"}
    return sum(score_parts([("in", part)], workflows))


if __name__ == "__main__":
    assert part1("day19_sample.txt") == 19114
    assert part1("day19.txt") == 397061

    assert part2("day19_sample.txt") == 167409079868000
    assert part2("day19.txt") == 125657431183201
