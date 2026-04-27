# Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses

# question: why is this problem a good candidate for DP, while the permutation and subsequence problems
# from @powerset.py are not?

from typing import List


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        # There will be many duplicated subproblems where we ask all the ways n parentheses can be formed.
        # This naturally lends to DP, bottom up is probably the most intuitive
        dp = [[], ["()"]]  # i = num parenthesis, dp[i] = a list of all formations

        while len(dp) <= n:
            prev_formations = dp[-1]
            formations = []
            last = len(prev_formations) - 1
            for i, s in enumerate(prev_formations):
                formations.append("(" + s + ")")
                formations.append(s + "()")

                # the last one is always a sequence of non-overlapping parens, like ()(). We already added another in the line above, no need to do again
                if i != last:
                    formations.append("()" + s)
            dp.append(formations)

        return dp[n]


print(Solution().generateParenthesis(4))
