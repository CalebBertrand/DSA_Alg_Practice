# Given a grid of spaces where each space either holds n coins or a robber who steals n coins,
# what is the max profit possible for a robot traversing from the top left of the grid to the
# bottom right? The robot can only move right and down. The robot can also "neutralize" up to 2
# robbers, meaning that cell will result in no change to the robot's coins

from collections import deque
from typing import List


def max_not_none(x: int | None, y: int | None) -> int:
    if x is None and y is None:
        return 0
    if x is None:
        assert y is not None
        return y
    if y is None:
        assert x is not None
        return x
    return max(x, y)


class Payoffs:
    def __init__(self, width: int, height) -> None:
        self.table = [[None] * height for _ in range(width)]

    def get(self, x: int, y: int):
        return self.table[x][y]

    def set(self, x: int, y: int, value):
        self.table[x][y] = value


# general idea is instead of searching through the 2d grid, you actually have to search throu a 3d
# "cube" where the third dimension keeps track of the number of robbers you have neutralized. You
# can't just use a greedy alg and neutralize all robbers, because there might be a better one to neutralize later


class Solution:
    def maximumAmount(self, coins: List[List[int]]) -> int:
        # x:y -> [max payoffs with each # robbers neutralized]
        to_check = deque([(0, 0)])
        max_x = len(coins) - 1
        max_y = len(coins[0]) - 1
        payoffs = Payoffs(len(coins), len(coins[0]))

        while to_check:
            check_x, check_y = to_check.popleft()
            if payoffs.get(check_x, check_y) is not None:
                continue  # already finished this cell

            above_payoffs = (
                payoffs.get(check_x, check_y - 1) if check_y > 0 else [None] * 3
            )
            left_payoffs = (
                payoffs.get(check_x - 1, check_y) if check_x > 0 else [None] * 3
            )
            if above_payoffs is None or left_payoffs is None:
                to_check.append((check_x, check_y))
                continue

            cell_coins = coins[check_x][check_y]

            # the best you can do for each num of robbers neutralized previously
            cell_payoffs = [
                max_not_none(above_payoffs[i], left_payoffs[i]) + cell_coins
                for i in range(3)
            ]
            if cell_coins < 0:
                # the best we can do with using one more neutralization is the
                # higher between neutralizing this robber or the case of already neutralizing
                # another one in the past
                cell_payoffs[2] = max(cell_payoffs[2], cell_payoffs[1] - cell_coins)
                cell_payoffs[1] = max(cell_payoffs[1], cell_payoffs[0] - cell_coins)

            payoffs.set(check_x, check_y, cell_payoffs)

            if check_x < max_x:
                to_check.append((check_x + 1, check_y))
            if check_y < max_y:
                to_check.append((check_x, check_y + 1))

        final_payoffs = payoffs.get(max_x, max_y)
        assert final_payoffs is not None

        return final_payoffs[2]


print(Solution().maximumAmount([[10, -10, 10], [10, -10, 10]]))
