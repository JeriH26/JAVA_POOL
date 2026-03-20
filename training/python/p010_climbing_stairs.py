"""P010 Climbing Stairs
Time: O(n), Space: O(1)
"""

def solve(n):
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        prev2, prev1 = prev1, prev1 + prev2
    return prev1


if __name__ == '__main__':
    print(solve(2))
    print(solve(5))
