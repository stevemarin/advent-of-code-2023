from array import array
from dataclasses import dataclass
from os.path import dirname, join, pardir
from typing import Iterator

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
