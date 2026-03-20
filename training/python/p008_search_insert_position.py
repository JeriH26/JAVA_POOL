"""P008 Search Insert Position
Time: O(log n), Space: O(1)
"""

def solve(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return left


if __name__ == '__main__':
    print(solve([1, 3, 5, 6], 5))
    print(solve([1, 3, 5, 6], 2))
