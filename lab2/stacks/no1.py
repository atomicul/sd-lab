#!/usr/bin/env python3

from typing import List, NamedTuple


class StackValue(NamedTuple):
    idx: int
    value: int


_ = input()
nums = list(map(int, input().split()))

stack: List[StackValue] = []

result = [0 for _ in nums]

for i, num in reversed(list(enumerate(nums))):
    while stack:
        j, top = stack.pop()

        if num >= top:
            stack.append(StackValue(j, top))
            break

        result[j] = i + 1

    stack.append(StackValue(i, num))

print(*result)
