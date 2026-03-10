#!/usr/bin/env python3

import itertools

nums = map(int, input().split())

nums = list(itertools.accumulate(nums))

try:
    while True:
        l, r = map(int, input().split())

        s = nums[r]
        s -= nums[l-1] if l-1 >= 0 else 0

        print(s)
except EOFError:
    pass
