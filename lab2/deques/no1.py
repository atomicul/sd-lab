#!/usr/bin/env python3

from typing import Deque, NamedTuple, Sequence
import collections


class DeqValue(NamedTuple):
    idx: int
    value: int


def main():
    n = int(input())
    nums = list(map(int, input().split()))

    print(*solution(nums, n), sep="\n")


def solution(nums: Sequence[int], stride: int):
    deque: Deque[DeqValue] = collections.deque(maxlen=stride)

    for idx, num in enumerate(nums):
        relevant_floor = idx - stride + 1

        while deque and deque[0].idx < relevant_floor:
            deque.popleft()

        while deque and num <= deque[-1].value:
            deque.pop()

        deque.append(DeqValue(idx, num))

        window = nums[relevant_floor : idx + 1]
        if len(window) != stride:
            continue

        yield (window, deque[0].value)


if __name__ == "__main__":
    main()
