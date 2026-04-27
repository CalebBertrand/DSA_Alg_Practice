# Given strings s and t, return the number of ways t can be formed by picking distinct sequences (left to right)
# of characters from s

from collections import deque


class Solution1:
    def numDistinct(self, s: str, t: str) -> int:
        n = 0
        q = deque([(0, 0)])
        while q:
            s_i, t_i = q.popleft()

            match = s[s_i] == t[t_i]
            done = t_i == len(t) - 1
            if match and done:
                n = n + 1

            # in both cases, we'll check the not included path
            if s_i < len(s) - 1:
                q.append((s_i + 1, t_i))
                if match and not done:
                    q.append((s_i + 1, t_i + 1))
        return n


# Why doesn't the above solution run fast enough?
# It actually checks the same sub paths many many times, in other words it does not
# take advantage of any memoization. Important lesson for DP problems: you won't be able
# to use memoization unless you build the paths in small increments that connect to each other.
# In the above solution, each path runs to completion without any reference to other paths


class Solution2:
    def numDistinct(self, s: str, t: str) -> int:
        assert len(s) >= len(t)
        # read: how many ways can I read i in source string, and be j characters through the target string already?
        dp = [[0] * len(t) for _ in s]

        for i, source_char in enumerate(s):
            for j, target_char in enumerate(t):
                match = source_char == target_char
                first_target_char = j == 0
                first_source_char = i == 0

                if not first_source_char:
                    dp[i][j] = dp[i - 1][j]
                if match:
                    if first_target_char:
                        dp[i][j] = dp[i][j] + 1
                    # assuming there is at least one way to get here in the first place
                    elif not first_source_char and dp[i - 1][j - 1] > 0:
                        dp[i][j] = dp[i][j] + dp[i - 1][j - 1]
        return dp[-1][-1]
