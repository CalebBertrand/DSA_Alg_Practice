# Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Set


@dataclass(slots=True)
class Rank:
    prev: Rank | None
    next: Rank | None
    items: Set[int]


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        if not len(nums) or k == 0:
            return []

        # a bucket of all the items that appear just once, each .prev being a bucket where they appear +1 times
        bottom = Rank(None, None, {nums[0]})

        # the top of the list, which should contain the things that appear the most
        root = bottom

        # a shortcut to each rank for each number that has appeared so far
        num_ranks = {nums[0]: bottom}

        for i in range(1, len(nums)):
            num = nums[i]
            rank = num_ranks.get(num)
            if rank:
                if rank.prev:
                    rank.prev.items.add(num)
                else:
                    rank.prev = Rank(None, rank, {num})
                    root = rank.prev

                num_ranks[num] = rank.prev
                rank.items.remove(num)
            else:
                num_ranks[num] = bottom
                bottom.items.add(num)

        result = []
        for _ in range(k):
            while not len(root.items):
                assert root.next
                root = root.next
            result.append(root.items.pop())
        return result


# expect [2, 1, 5] or [2, 5, 1]
print(Solution().topKFrequent([1, 1, 2, 3, 2, 5, 2, 36, 423, 5, 1], 3))

# expect [3, 5]
print(Solution().topKFrequent([5, 2, 5, 3, 5, 3, 1, 1, 3], 2))

# expect [1, 3]
print(Solution().topKFrequent([5, 3, 1, 1, 1, 3, 73, 1], 2))


# reflection: this is technically O(n), but is it actually a very good solution?
# the standard answer to this problem is bucket sort, why might that be preferred to my first attempt with a linked list?
# Why is bucket sort a good candidate for this problem (think of bucket sort's main limitation)?
