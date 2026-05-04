# You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
# Merge all the linked-lists into one sorted linked-list and return it.
#
#

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List
import math
from itertools import pairwise


@dataclass(eq=False, slots=True)
class ListNode:
    val: int | float
    next: Optional[ListNode]


class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None

        dummy_root = ListNode(-math.inf, None)
        tail = dummy_root
        heads = lists

        while len(heads) > 1:
            next_heads = []

            # it just so happens that the built in python sort uses Timsort, an algorithm which does well on mostly already sorted lists
            heads.sort(key=lambda n: n.val if n is not None else math.inf)
            last = heads[-1]

            stop_point = math.inf
            for curr, bigger in pairwise(heads):
                if bigger is not None:
                    while (
                        curr is not None
                        and curr.val < stop_point
                        and curr.val <= bigger.val
                    ):
                        tail.next = curr
                        tail = curr
                        curr = curr.next

                if curr:
                    next_heads.append(curr)
                    stop_point = min(stop_point, curr.val)

            if last:
                next_heads.append(last)
            heads = next_heads

        if not heads:
            return None
        tail.next = heads[0]

        return dummy_root.next


# expect [1, 1, 3, 4, 5, 6, 7, 8, 9, 10, 57]
print(
    Solution().mergeKLists(
        [
            ListNode(1, ListNode(4, ListNode(57, None))),
            ListNode(3, ListNode(5, None)),
            ListNode(
                1,
                ListNode(6, ListNode(7, ListNode(8, ListNode(9, ListNode(10, None))))),
            ),
        ]
    )
)

# expect [-10, -10, -8, -7, -7, -7, -5, -2, 0, 1, 1, 1, 2, 3, 4]
print(
    Solution().mergeKLists(
        [
            ListNode(
                -8,
                ListNode(
                    -7,
                    ListNode(
                        -7,
                        ListNode(
                            -5, ListNode(1, ListNode(1, ListNode(3, ListNode(4, None))))
                        ),
                    ),
                ),
            ),
            ListNode(-2, None),
            ListNode(
                -10,
                ListNode(
                    -10, ListNode(-7, ListNode(0, ListNode(1, ListNode(3, None))))
                ),
            ),
            ListNode(2, None),
        ]
    )
)

# expect [1]
print(Solution().mergeKLists([None, ListNode(1, None)]))


# reflection: why did I opt for a full sort on the heads each iteration, and why did it actually result in decent performance?
# if I wanted to get optimal time complexity, what could I use instead of a sorted list for the heads?
