"""P001 Two Sum Practice
TODO: implement solve(nums, target)
"""


def solve(nums, target):
    #raise NotImplementedError("TODO: implement p001 two sum")
    #seen = {}
    #for i, num in enumerate(nums):
    #    need = target - num
    #    if need in seen:
    #        return [seen[need], i]
    #    seen[num] = i
    #return []

    n = len(nums)
    for i in range(n):
        for j in range(i+1, n):
            if nums[i] + nums[j] == target:
                return [i,j]
    return[]



if __name__ == '__main__':
    print(solve([2, 11, 7, 15], 9))  # expected: [0, 1]
