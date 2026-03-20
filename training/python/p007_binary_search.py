"""P007 Binary Search
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
    return -1


if __name__ == '__main__':
    print(solve([-1, 0, 3, 5, 9, 12], 9))
    print(solve([-1, 0, 3, 5, 9, 12], 2))
