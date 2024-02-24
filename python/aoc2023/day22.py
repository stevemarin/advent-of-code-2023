from dataclasses import dataclass
from os.path import join

from aoc2023 import DATA_DIR


@dataclass
class Tower:
    num_rows: int
    num_cols: int
    slices: list[list[int]]

    def __getitem__(self, idx: int) -> list[int]:
        return self.slices[idx]

    def __len__(self) -> int:
        return len(self.slices)

    def add_block_at_z(self, block: "Block", z: int) -> None:
        assert 0 <= z < len(self)

        slices = self.slices
        if block.z.start != block.z.stop:
            idx = block.y.start * self.num_cols + block.x.start
            for z_idx in range(z, block.z.stop - block.z.start):
                assert slices[z_idx][idx] == 0
                slices[z_idx][idx] = block.id
        if block.y.start != block.y.stop:
            for col in range(block.y.start, block.y.stop + 1):
                idx = row * self.num_cols + col


        return None


@dataclass
class Block:
    id: int
    x: range
    y: range
    z: range

    def __post_init__(self) -> None:
        x = 0 if len(self.x) else 1
        y = 0 if len(self.y) else 1
        z = 0 if len(self.z) else 1
        assert x + y + z == 1

    @staticmethod
    def from_str(id: int, s: str) -> "Block":
        (x1, y1, z1), (x2, y2, z2) = (map(int, ss.split(",")) for ss in s.split("~"))
        return Block(id, range(x1, x2 + 1), range(y1, y2 + 1), range(z1, z2 + 1))

    def __lt__(self, other: "Block") -> bool:
        return True if self.z.start < other.z.start else False

    def to_slice(self, num_rows: int, num_cols: int) -> list[int]:
        if self.z.start != self.z.stop:
            rows_cols = [(self.y.start, self.x.start)]
        elif self.x.start == self.x.stop:
            rows_cols = [(y, self.x.start) for y in range(self.y.stop + 1)]
        else:
            rows_cols = [(self.y.start, x) for x in range(self.x.stop + 1)]

        indices = [row * num_cols + col for row, col in rows_cols]

        # print(num_cols)
        # for (row, col), idx in zip(rows_cols, indices):
        #     print(row, col, idx)

        s = [0] * num_rows * num_cols
        for idx in indices:
            s[idx] = self.id

        return s


def get_touching(block: list[int], tower_slice: list[int]) -> set[int]:
    touches = set()
    for b, s in zip(block, tower_slice):
        if b != 0 and s != 0:
            touches.add(s)
    return touches


def read_input(filename: str) -> list[Block]:
    blocks = []
    with open(join(DATA_DIR, filename), "r") as fh:
        for idx, line in enumerate(fh.read().strip().split("\n")):
            blocks.append(Block.from_str(idx + 1, line.strip()))

    return blocks


if __name__ == "__main__":
    blocks = read_input("day22_sample.txt")

    for block in blocks:
        assert block.x.start <= block.x.stop
        assert block.y.start <= block.y.stop
        assert block.z.start <= block.z.stop

    xmin = min(block.x.start for block in blocks)
    xmax = max(block.x.stop for block in blocks)
    ymin = min(block.y.start for block in blocks)
    ymax = max(block.y.stop for block in blocks)
    zmin = 1
    zmax = max(block.z.stop for block in blocks)

    assert xmin == ymin == 0

    tower = Tower(ymax + 1, xmax + 1, [[0] * (xmax + 1) * (ymax + 1)] * zmax)

    block_slices = [block.to_slice(ymax + 1, xmax + 1) for block in blocks]

    for block_slice in block_slices:
        for idx in range(0, 9, 3):
            print(block_slice[idx : idx + 3])
        print()

    for block, block_slice in zip(blocks, block_slices):
        # fall until we hit the bottom or we hit something
        z, touching = block.z.start, set()
        while len(touching) == 0 and z >= 1:
            touching = get_touching(block_slice, tower[z - 1])
            z -= 1

        # make sure the only time there're no intersections
        # is when they hit the bottom
        if len(touching) == 0 and z != 0:
            raise NotImplementedError

        tower.add_block_at_z(block, z)

        for tower_slice in tower:
            for idx in range(0, 9, 3):
                print(tower_slice[idx : idx + 3])
            print()
