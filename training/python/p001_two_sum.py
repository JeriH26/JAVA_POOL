"""P001 Two Sum
Time: O(n), Space: O(n)
"""

def solve(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        need = target - num
        if need in seen:
            return [seen[need], i]
        seen[num] = i
    return []


if __name__ == '__main__':
    print(solve([2, 7, 11, 15], 9))
