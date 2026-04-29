#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Iterable, List, NamedTuple, Sequence


class StackValue(NamedTuple):
    idx: int
    value: int


def main():
    histogram = [int(x) for x in input().split()]

    print(max(box.area for box in boxes(histogram)))


def boxes(histogram: Sequence[int]) -> Iterable["Box"]:
    stack: List[StackValue] = []

    for i, line in enumerate(histogram):
        while stack:
            j, top = stack[-1]

            if line >= top:
                break

            stack.pop()
            yield Box(j, i, top)

        stack.append(StackValue(i, line))

    for pos, height in stack:
        yield Box(pos, len(histogram) - 1, height)


if __name__ == "__main__":
    main()


@dataclass
class Box:
    start_index: int
    end_index: int
    height: int

    @property
    def width(self):
        return self.end_index - self.start_index + 1

    @property
    def area(self):
        return self.width * self.height
