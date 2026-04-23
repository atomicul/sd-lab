#!/usr/bin/env python3

import sys
from typing import AbstractSet, NamedTuple, Optional
from collections import deque
from itertools import product


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self.x + other.x, self.y + other.y)


def main():
    size = int(input())
    start = Point(*map(int, input().split()))
    end = Point(*map(int, input().split()))

    if not all(is_contained(size, p) for p in [start, end]):
        sys.exit(1)

    obstacles = {Point(*map(int, line.split())) for line in sys.stdin.readlines()}
    obstacles -= {p for p in obstacles if not is_contained(size, p)}

    path = lee(size, start, end, obstacles)
    print_map(size, start, end, frozenset(path), obstacles)


def lee(size: int, start: Point, end: Point, obstacles: AbstractSet) -> list[Point]:
    queue = deque([start])
    visitied_from: dict[Point, Optional[Point]] = {start: None}

    def build_path(pos: Optional[Point]):
        if pos is None:
            return

        yield from build_path(visitied_from[pos])
        yield pos

    while queue:
        pos = queue.popleft()

        if pos == end:
            return list(build_path(pos))

        deltas = product(*(2 * [(-1, 0, 1)]))
        deltas = (Point(dx, dy) for dx, dy in deltas if dx == 0 or dy == 0)
        neighbours = (pos + delta for delta in deltas)

        for neighbour in neighbours:
            if not is_contained(size, neighbour):
                continue

            if neighbour in visitied_from.keys() | obstacles:
                continue

            visitied_from[neighbour] = pos
            queue.append(neighbour)

    return []


def is_contained(size: int, point: Point) -> bool:
    return all(0 <= coordinate < size for coordinate in point)


def print_map(
    size: int,
    start: Point,
    end: Point,
    path: AbstractSet[Point],
    obstacles: AbstractSet[Point],
):
    for y in range(size):
        for x in range(size):
            p = Point(x, y)

            if p == start:
                print("S", end=" ")
            elif p == end:
                print("F", end=" ")
            elif p in obstacles:
                print("X", end=" ")
            elif p in path:
                print("0", end=" ")
            else:
                print(".", end=" ")
        print()


if __name__ == "__main__":
    main()
