"""P006 Valid Parentheses
Time: O(n), Space: O(n)
"""


def solve(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
        else:
            stack.append(ch)
    return len(stack) == 0


if __name__ == '__main__':
    print(solve('()[]{}'))
    print(solve('(]'))
