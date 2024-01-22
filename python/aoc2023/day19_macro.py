from os.path import join
from textwrap import dedent
from types import FunctionType

from aoc2023 import DATA_DIR

PREFIX = "_"


def create_pipeline_function(pipeline: str) -> tuple[str, FunctionType]:
    def get_step(step: str) -> str:
        if ":" not in step:
            return dedent(
                f"""\
                {f"return '{step}'" if step in ("A", "R") else "return funcs['" + PREFIX + step + "'](part, funcs)"}
            """
            )

        op = ">" if ">" in step else "<"
        param, rest = step.split(op)
        value, target = rest.split(":")

        return dedent(
            f"""\
            if "{param}" in part:
              if part["{param}"] {op} {value}:
                {f"return '{target}'" if target in ("A", "R") else "return funcs['" + PREFIX + target + "'](part, funcs)"}
            """
        )

    name, rest = pipeline.split("{")
    name = PREFIX + name
    steps = rest[:-1].split(",")

    func = ""
    for step in steps:
        func += get_step(step)

    func = (
        dedent(
            f"""\
        def {name}(part, funcs):
    """
        )
        + "\n"
        + "\n".join(["  " + line for line in func.split("\n")])
    )

    func_obj = compile(func, "<string>", "exec")
    func = FunctionType(func_obj.co_consts[0], globals(), name)

    return name, func


def read_input(filename: str):
    with open(join(DATA_DIR, filename), "r") as fh:
        top, bottom = fh.read().strip().split("\n\n")

    pipelines = top.split("\n")

    funcs = {}
    for pipeline in pipelines:
        name, func = create_pipeline_function(pipeline)
        funcs[name] = func

    parts_str = bottom.split("\n")

    parts = []
    for part_str in parts_str:
        part = {}
        for kv in part_str[1:-1].split(","):
            k, v = kv.split("=")
            part[k] = int(v)
        parts.append(part)

    return funcs, parts


def part1(filename: str) -> int:
    funcs, parts = read_input(filename)

    first = funcs[PREFIX + "in"]

    passing = []
    for part in parts:
        if first(part, funcs) == "A":
            passing.append(part)

    return sum(map(lambda x: sum(x.values()), passing))


def part2(filename: str) -> int:
    funcs, _ = read_input(filename)

    first = funcs[PREFIX + "in"]

    passing = []
    part = {char: range(1, 4001) for char in "xmas"}
    if first(part, funcs) == "A":
        passing.append(part)

    return sum(map(lambda x: sum(x.values()), passing))


if __name__ == "__main__":
    assert part1("day19_sample.txt") == 19114
    assert part1("day19.txt") == 397061

    print(part2("day19_sample.txt"))
