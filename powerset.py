# Given an integer array nums of unique elements, return all possible subsets (the power set).
# The solution set must not contain duplicate subsets. Return the solution in any order.

from typing import List, Set


class PowersetSolution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = [[]]

        # notice that all subsets are actually just one of the previous ones, plus a new number.
        # if we loop through each number and only add them in order, we can be sure there are no duplicates
        # general idea is: for each number, take everything we've discovered so far, and add those+the next number to the result

        for num in nums:
            result += [subset + [num] for subset in result]

        return result


print("Powersets: ", PowersetSolution().subsets([1, 2, 3]))


# what if it is all possible permutations, not subsets? (meaning order matters)
# In that case we can't just have one outer loop going over the numbers, and "traversing"
# the possible combinations is unavoidable


class PermutationsSolution:
    def _permuteRec(
        self, prev: List[int] = [], used: Set[int] = set()
    ) -> List[List[int]]:
        # base case, at the end of the list
        if len(used) == len(self.nums) - 1:
            return [prev + [n] for n in self.nums if n not in used]

        return [
            subsequence
            for n in self.nums
            if n not in used
            for subsequence in self._permuteRec(prev + [n], used.union({n}))
        ]

    def permute(self, nums: List[int]) -> List[List[int]]:
        self.nums = nums
        return self._permuteRec()


print("Permutations: ", PermutationsSolution().permute([1, 2, 3]))

# okay, that gives a permutations. What about all possible subsequences, meaning including sequences shorter than the original list?
# it will be similar, but in our traversal we need to consider the option of not including n


# question: why is this NOT a DP problem?


class SubsequencesSolution:
    def _subsequencesRec(
        self, prev: List[int] = [], used: Set[int] = set()
    ) -> List[List[int]]:
        return [prev] + [
            subsequence
            for n in self.nums
            if n not in used
            for subsequence in self._subsequencesRec(prev + [n], used.union({n}))
        ]

    def subsequences(self, nums: List[int]) -> List[List[int]]:
        self.nums = nums
        return self._subsequencesRec()


print("Subsequences: ", SubsequencesSolution().subsequences([1, 2, 3]))
