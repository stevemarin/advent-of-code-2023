# from dataclasses import dataclass, field
# from operator import gt, lt
# from os.path import join
# from typing import Callable

# from aoc2023 import DATA_DIR


# @dataclass
# class Range:
#     low: int
#     high: int


# @dataclass
# class Part:
#     x: Range
#     m: Range
#     a: Range
#     s: Range


# @dataclass
# class PipelineStep:
#     rating: str
#     op: Callable[[int, int], bool]
#     value: int
#     target: str


# @dataclass
# class Pipeline:
#     steps: list[PipelineStep] = field(default_factory=list)
#     default: str = ""

#     def process(part: Part) ->


# def read_input(filename: str) -> tuple[dict[str, Pipeline], list[Part]]:
#     with open(join(DATA_DIR, filename), "r") as fh:
#         top, bottom = fh.read().strip().split("\n\n")

#     pipelines: dict[str, Pipeline] = {}
#     for pipeline_str in top.split("\n"):
#         name, rest = pipeline_str.split("{")
#         pipeline_steps = rest[:-1].split(",")

#         pipeline = Pipeline([])
#         for step in pipeline_steps[:-1]:
#             op_str = ">" if ">" in step else "<"
#             op = gt if ">" in step else lt
#             rating, rest = step.split(op_str)
#             assert rating in "xmas"
#             value_str, target = rest.split(":")
#             pipeline.steps.append(PipelineStep(rating, op, int(value_str), target))

#         pipeline.default = pipeline_steps[-1]
#         pipelines[name] = pipeline

#     parts = []
#     for part_str in bottom.split("\n"):
#         x, m, a, s = Range(-1, -1), Range(-1, -1), Range(-1, -1), Range(-1, -1)
#         for kv in part_str[1:-1].split(","):
#             rating, value_str = kv.split("=")
#             value = int(value_str)
#             match rating:
#                 case "x":
#                     x = Range(value, value)
#                 case "m":
#                     m = Range(value, value)
#                 case "a":
#                     a = Range(value, value)
#                 case "s":
#                     s = Range(value, value)

#         part = Part(x, m, a, s)

#         for attr in "xmas":
#             assert getattr(part, attr).low >= 0

#         parts.append(part)

#     return pipelines, parts


# if __name__ == "__main__":
#     pipelines, parts = read_input("day19_sample.txt")
#     for k, v in pipelines.items():
#         print(k)
#         for _ in v.steps:
#             print("", _)
#     # assert part1("day19_sample.txt") == 19114
#     # assert part1("day19.txt") == 397061

#     # print(part2("day19_sample.txt"))
#     # assert part2("day19_sample.txt") == 167409079868000
#     # print(part2("day19.txt"))

#     # 167409079868000
#     # 130857687958725
#     # 255999999987500
