from enum import IntEnum
from math import lcm
from os.path import join
from queue import Queue
from typing import Callable

from aoc2023 import DATA_DIR


class Pulse(IntEnum):
    Low = 0
    High = 1


class State(IntEnum):
    Off = 0
    On = 1


ProcessPulse = Callable[[str, Pulse, Queue], Queue]


def get_flip_flop(name: str, outgoing: list[str]) -> ProcessPulse:
    state = State.Off

    def process_pulse(_0: str, pulse: Pulse, q: Queue) -> Queue:
        nonlocal state

        match pulse, state:
            case Pulse.High, _:
                return q
            case Pulse.Low, State.Off:
                state = State.On
                p = Pulse.High
            case Pulse.Low, State.On:
                state = State.Off
                p = Pulse.Low

        for next_node in outgoing:
            q.put((name, next_node, p))

        return q

    return process_pulse


def get_conjunction(
    name: str, incoming: list[str], outgoing: list[str]
) -> ProcessPulse:
    states = {c: Pulse.Low for c in incoming}

    def process_pulse(from_node: str, pulse: Pulse, q: Queue) -> Queue:
        states[from_node] = pulse
        if all([p == Pulse.High for p in states.values()]):
            p = Pulse.Low
        else:
            p = Pulse.High

        for next_node in outgoing:
            q.put((name, next_node, p))

        return q

    return process_pulse


def get_dummy() -> ProcessPulse:
    def process_pulse(_0: str, _1: Pulse, q: Queue) -> Queue:
        return q

    return process_pulse


def get_broadcaster(name: str, outgoing: list[str]) -> ProcessPulse:
    def process_pulse(_0: str, _1: Pulse, q: Queue) -> Queue:
        for c in outgoing:
            q.put((name, c, Pulse.Low))

        return q

    return process_pulse


def press_button(nodes: dict[str, ProcessPulse], idx: int) -> tuple[int, int]:
    q = Queue()
    q = nodes["broadcaster"]("", Pulse.Low, q)

    low_count = 1  # to capture buttom->broadcaster
    high_count = 0

    while not q.empty():
        pulse: Pulse
        name, next_node, pulse = q.get()

        # getting cycle lengths
        # if name in {"vr", "nl", "lr", "gt"} and pulse == Pulse.High:
        # print(idx, name, pulse)

        if pulse == Pulse.Low:
            low_count += 1
        else:
            high_count += 1

        # print(name, next_node, pulse)
        nodes[next_node](name, pulse, q)

    return low_count, high_count


def read_input(filename: str) -> dict[str, ProcessPulse]:
    with open(join(DATA_DIR, filename), "r") as fh:
        lines = fh.read().strip().split("\n")

    node_data = {}
    for line in lines:
        if line[0] not in ("&", "%"):
            parts = line.split(" -> ")
            assert parts[0] == "broadcaster"
            node_data[parts[0]] = {
                "incoming": [],
                "outgoing": parts[1].split(", "),
                "type": "broadcaster",
            }
        else:
            parts = line.split(" -> ")
            node_data[parts[0][1:]] = {
                "incoming": [],
                "outgoing": parts[1].split(", "),
                "type": "flip_flop" if parts[0][0] == "%" else "conjunction",
            }

    # handle sample 2 dummy node
    node_data["output"] = {"incoming": [], "outgoing": [], "type": "dummy"}

    # rx is a dummy node
    node_data["rx"] = {"incoming": [], "outgoing": [], "type": "dummy"}

    for name in node_data.keys():
        for outgoing in node_data[name]["outgoing"]:
            node_data[outgoing]["incoming"].append(name)

    nodes = {}
    for name, node in node_data.items():
        match node["type"]:
            case "flip_flop":
                nodes[name] = get_flip_flop(name, node["outgoing"])
            case "conjunction":
                nodes[name] = get_conjunction(name, node["incoming"], node["outgoing"])
            case "broadcaster":
                nodes[name] = get_broadcaster(name, node["outgoing"])
            case "dummy":
                nodes[name] = get_dummy()

    return nodes


def part1(filename: str) -> int:
    nodes = read_input(filename)

    low_count, high_count = 0, 0
    for idx in range(1000):
        low, high = press_button(nodes, idx)
        low_count += low
        high_count += high

    return low_count * high_count


def part2(filename: str) -> None:
    # don't forget to uncomment printing in press_button
    # to get cycle lengths
    nodes = read_input(filename)

    for idx in range(15000):
        _ = press_button(nodes, idx)


if __name__ == "__main__":
    assert part1("day20_sample1.txt") == 32000000
    assert part1("day20_sample2.txt") == 11687500
    assert part1("day20.txt") == 912199500

    # uncomment to calculate cycle lengths
    # part2("day20.txt")

    cycles = {"vr": 3907, "nl": 4003, "lr": 3889, "gt": 3911}
    assert lcm(*cycles.values()) == 237878264003759
