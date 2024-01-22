from array import array
from dataclasses import dataclass
from os.path import dirname, join, pardir
from typing import Any, Iterable, Iterator

DATA_DIR = join(dirname(__file__), pardir, pardir, "data")


@dataclass
class NDArray[T: str | int | float]:
    num_rows: int
    num_cols: int
    _data: array

    def __repr__(self) -> str:
        idx = 0
        lines: list[str] = []
        for _ in range(self.num_rows):
            lines.append("".join(map(str, self._data[idx : idx + self.num_cols])))
            idx += self.num_cols
        return "\n".join(lines)

    def __getitem__(self, item: int) -> T:
        return self._data[item]

    def __len__(self) -> int:
        return len(self._data)

    def iterrows(self) -> Iterator[array]:
        for row in range(self.num_rows):
            start = row * self.num_cols
            stop = start + self.num_cols
            yield self._data[start:stop:1]

    def itercols(self) -> Iterator[array]:
        step = self.num_cols
        for col in range(self.num_cols):
            start = col
            stop = start + self.num_cols * (self.num_rows - 1) + 1
            yield self._data[start:stop:step]

    def transpose(self) -> "NDArray":
        num_rows, num_cols = self.num_cols, self.num_rows
        data = array(
            self._data.typecode, [item for col in self.itercols() for item in col]
        )
        return NDArray(num_rows, num_cols, data)

    def reverse_rows(self) -> "NDArray":
        _data = [item for row in self.iterrows() for item in reversed(row)]
        return NDArray(self.num_rows, self.num_cols, array(self._data.typecode, _data))

    def reverse_cols(self) -> "NDArray":
        _data = [item for col in self.itercols() for item in reversed(col)]
        return NDArray(
            self.num_cols, self.num_rows, array(self._data.typecode, _data)
        ).transpose()

    def flip(self) -> "NDArray":
        _data = self._data
        _data.reverse()
        return NDArray(
            self.num_rows,
            self.num_cols,
            _data,
        )

    def rotate_clockwise(self) -> "NDArray":
        _data = [item for col in self.itercols() for item in reversed(col)]
        return NDArray(
            self.num_cols,
            self.num_rows,
            array(self._data.typecode, _data),
        )

    def rotate_counterclockwise(self) -> "NDArray":
        _data = [item for col in self.iterrows() for item in reversed(col)]
        return NDArray(
            self.num_rows,
            self.num_cols,
            array(self._data.typecode, _data),
        ).transpose()

    def idx_to_row_col(self, idx: int) -> tuple[int, int]:
        return divmod(idx, self.num_cols)

    def row_col_to_idx(self, row: int, col: int) -> int:
        return row * self.num_cols + col


@dataclass
class Range:
    start: int
    end: int
    label: str | None = None

    def __post_init__(self):
        # assert ranges are increasing
        if self.end < self.start:
            self.start, self.end = self.end, self.start

    def intersection(self, other: "Range") -> "Range | None":
        if not self.intersects(other):
            return None

        return Range(max(self.start, other.start), min(self.end, other.end))

    def intersects(self, other: "Range") -> bool:
        if self.start > other.end or self.end < other.start:
            return False
        else:
            return True

    def split_after(self, value: int) -> list["Range"]:
        if value not in self:
            raise ValueError("cannot split with external point")
        return [Range(self.start, value), Range(value + 1, self.end)]

    def contains(self, other: "Range") -> bool:
        return other.start >= self.start and other.end <= self.end

    def shift_by(self, value: int) -> "Range":
        return Range(self.start + value, self.end + value)

    def __contains__(self, value: int) -> bool:
        return self.start <= value <= self.end

    def __add__(self, other: "Range") -> list["Range"]:
        if self.intersects(other):
            return [Range(min(self.start, other.start), max(self.end, other.end))]
        elif self.start < other.start:
            return [self, other]
        else:
            return [other, self]

    def __sub__(self, other: "Range") -> list["Range"] | None:
        intersection = self.intersection(other)
        if intersection is None:
            return [self]
        elif intersection == self:
            return None
        elif intersection.start == self.start:
            return [Range(intersection.end, self.end)]
        elif intersection.end == self.end:
            return [Range(self.start, intersection.start)]
        else:
            return [
                Range(self.start, intersection.start),
                Range(intersection.end, self.end),
            ]

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Range):
            return self.start == other.start and self.end == other.end
        else:
            raise NotImplementedError("cannot equate Range with another type")

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __len__(self) -> int:
        return self.end - self.start

    def __iter__(self) -> Iterable[int]:
        for _ in range(self.start, self.end):
            yield _


# @dataclass
# class NDRange:
#     ranges: list[Range]

#     def intersection(self: Self, other: Self) -> Self | None:
#         self_labels = [r.label for r in self.ranges]
#         other_labels = [r.label for r in other.ranges]
#         assert self_labels == other_labels

#         ranges = []
#         for self_range, other_range in zip(self.ranges, other.ranges):
#             range_ = self_range.intersection(other_range)
#             if range_ is None:
#                 return None
#             else:
#                 range_.label = self_range.label
#                 ranges.append(range_)

#         return NDRange(ranges)

#     def union(self: Self, other: Self) -> [NDRange]:
#         pass


# if __name__ == "__main__":
#     a = NDRange([Range(2, 3, "x"), Range(0, 3, "y")])
#     b = NDRange([Range(0, 3, "x"), Range(2, 4, "y")])
#     i = NDRange([Range(2, 3, "x"), Range(2, 3, "y")])
#     u = NDRange([Range(0, 3, "x"), Range(0, 4, "y")])

#     assert a.intersection(b) == i
#     assert a.union(b) == u
