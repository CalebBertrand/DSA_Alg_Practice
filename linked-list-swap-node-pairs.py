# Given a linked list, swap every two adjacent nodes and return its head.
# You must solve the problem without modifying the values in the list's nodes (i.e., only nodes themselves may be changed.)
#
# Example:
# Input: head = [1,2,3,4]
# Output: [2,1,4,3]

from __future__ import annotations
from typing import Optional
from dataclasses import dataclass


@dataclass(slots=True, eq=False)
class ListNode:
    val: int = 0
    next: ListNode | None = None


class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return None

        prev = None
        first = head
        second = head.next
        root = second or first
        while first and second:
            next_first = second.next
            second.next = first
            first.next = next_first
            if prev is not None:
                prev.next = second

            prev = first
            first = next_first
            second = next_first.next if next_first is not None else None

        return root


# expect [2, 1, 4, 3]
print(Solution().swapPairs(ListNode(1, ListNode(2, ListNode(3, ListNode(4))))))
