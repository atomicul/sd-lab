#!/usr/bin/env python3

from typing import Iterable, Sequence, Tuple


def main():
    s = int(input())
    nums = list(map(int, input().split()))

    _, best_pair = min(ranges(nums, s), key=lambda x: x[0])
    print(*best_pair)


def ranges(nums: Sequence[int], target_sum: int) -> Iterable[Tuple[int, Tuple[int, int]]]:
    l = 0
    r = len(nums) - 1

    while l<r:
        s = nums[l] + nums[r]
        yield (abs(target_sum - s), (l, r))

        if s < target_sum:
            l += 1
        elif s > target_sum:
            r -= 1
        else:
            return


if __name__ == "__main__":
    main()
