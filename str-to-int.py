# Implement the myAtoi(string s) function, which converts a string to a 32-bit signed integer.
#
# The algorithm for myAtoi(string s) is as follows:
#
#     Whitespace: Ignore any leading whitespace (" ").
#     Signedness: Determine the sign by checking if the next character is '-' or '+', assuming positivity if neither present.
#     Conversion: Read the integer by skipping leading zeros until a non-digit character is encountered or the end of the string is reached. If no digits were read, then the result is 0.
#     Rounding: If the integer is out of the 32-bit signed integer range [-231, 231 - 1], then round the integer to remain in the range. Specifically, integers less than -231 should be rounded to -231, and integers greater than 231 - 1 should be rounded to 231 - 1.
#
# Return the integer as the final result.

digit_map = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}

max_int = (1 << 31) - 1
min_int = -(1 << 31)


class Solution:
    def myAtoi(self, s: str) -> int:
        acc = 0
        if not len(s):
            return acc

        is_negative = False
        i = 0
        while s[i] == " ":
            i = i + 1
            if i >= len(s):
                return acc

        if s[i] == "-":
            is_negative = True
            i = i + 1
        elif s[i] == "+":
            i = i + 1

        while i < len(s) and s[i] == "0":
            i = i + 1

        while i < len(s):
            n = digit_map.get(s[i])
            if n is None:
                break
            acc = (acc * 10) + n
            if is_negative and -acc <= min_int:
                return min_int
            if not is_negative and acc >= max_int:
                return max_int
            i = i + 1

        return -acc if is_negative else acc


print(Solution().myAtoi("  0004032"))  # expect 4032
print(Solution().myAtoi("-91283472332"))  # expect min_int
print(Solution().myAtoi("-2147483648"))  # expect -2147483648

# possibly could have implemented in a more readable structure, for example using a state machine in a while i < len(s). But this would have likely hurt performance.
# The cost is there are several places where we check i against the lenth of s
