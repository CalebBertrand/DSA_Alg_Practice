# Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.
# An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume
# all four edges of the grid are all surrounded by water.
#
# Examples:
#
# Input: grid = [
#   ["1","1","1","1","0"],
#   ["1","1","0","1","0"],
#   ["1","1","0","0","0"],
#   ["0","0","0","0","0"]
# ]
# Output: 1
#
# Input: grid = [
#   ["1","1","0","0","0"],
#   ["1","1","0","0","0"],
#   ["0","0","1","0","0"],
#   ["0","0","0","1","1"]
# ]
# Output: 3

from __future__ import annotations
from typing import List
from dataclasses import dataclass


@dataclass(eq=False)  # we actually rely on reference equality to tell them apart
class IslandCell:
    depth: int
    parent: IslandCell | None = None

    def root(self):
        if self.parent is None:
            return self
        return self.parent.root()


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        # used to keep the trees as balanced as possible
        island_map: List[List[None | IslandCell]] = [
            [None] * len(grid[0]) for _ in grid
        ]
        n = 0
        for i, row in enumerate(grid):
            for j, value in enumerate(row):
                if value == "1":
                    top = island_map[i - 1][j] if i != 0 else None
                    left = island_map[i][j - 1] if j != 0 else None

                    if top and left:
                        left_root, top_root = left.root(), top.root()
                        if left_root == top_root:
                            island_map[i][j] = IslandCell(0, left_root)
                            continue

                        if left_root.depth > top_root.depth:
                            top_root.parent = left_root
                            left_root.depth = max(left_root.depth, top_root.depth + 1)
                            island_map[i][j] = IslandCell(0, left_root)
                        else:
                            left_root.parent = top_root
                            top_root.depth = max(top_root.depth, left_root.depth + 1)
                            island_map[i][j] = IslandCell(0, top_root)

                        # we just merged two islands which we previously thought were separate
                        n = n - 1
                    elif top:
                        island_map[i][j] = IslandCell(0, top.root())
                    elif left:
                        island_map[i][j] = IslandCell(0, left.root())
                    else:
                        island_map[i][j] = IslandCell(0, None)
                        n = n + 1

        return n


# expect 3
print(
    Solution().numIslands(
        [
            ["1", "1", "0", "0", "0"],
            ["1", "1", "0", "0", "0"],
            ["0", "0", "1", "0", "0"],
            ["0", "0", "0", "1", "1"],
        ]
    )
)

# expect 1
print(
    Solution().numIslands(
        [
            ["1", "1", "1", "1", "0"],
            ["1", "1", "0", "1", "0"],
            ["1", "1", "0", "0", "0"],
            ["0", "0", "0", "0", "0"],
        ]
    )
)

# expect 1
print(Solution().numIslands([["1", "1", "1"], ["0", "1", "0"], ["1", "1", "1"]]))

# expect 2
print(
    Solution().numIslands(
        [
            ["1", "1", "1", "1", "1", "0", "1", "1", "1", "1"],
            ["1", "0", "1", "0", "1", "1", "1", "1", "1", "1"],
            ["0", "1", "1", "1", "0", "1", "1", "1", "1", "1"],
            ["1", "1", "0", "1", "1", "0", "0", "0", "0", "1"],
            ["1", "0", "1", "0", "1", "0", "0", "1", "0", "1"],
            ["1", "0", "0", "1", "1", "1", "0", "1", "0", "0"],
            ["0", "0", "1", "0", "0", "1", "1", "1", "1", "0"],
            ["1", "0", "1", "1", "1", "0", "0", "1", "1", "1"],
            ["1", "1", "1", "1", "1", "1", "1", "1", "0", "1"],
            ["1", "0", "1", "1", "1", "1", "1", "1", "1", "0"],
        ]
    )
)

# reflection: why couldn't I simply +1 any time a new island is made, and -1 any time they happen to be different (and basically bypass the trouble of merging them)?
# My original attempt did something similar to this. It could be a problem if the same two chunks touch in multiple places (n - 1 more than once). But that could be bypassed by keeping
# track of insland connections. However that would still fail, because what if island 1 is connected to 2, but then 1 & 2 each independently connect to 3? that still calls n-1 more than once.
# To get around this, you have to start traversing connections, which is inefficient unless you have a direction predefined, like parent-child. So you end up re-inventing the tree
# solution. This should give some confidence it is in fact a "good" solution
