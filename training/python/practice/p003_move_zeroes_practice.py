"""P003 Move Zeroes Practice
TODO: implement solve(nums)
"""


def solve(nums):
    #raise NotImplementedError("TODO: implement p003 move zeroes")
    #write = 0
    #for read in range(len(nums)):
    #    if nums[read] != 0:
    #        nums[write], nums[read] = nums[read], nums[write]
    #        write += 1
    #return nums


    n = len(nums)
    i = 0
    for j in range(n):
        if nums[i] == 0:
            nums.pop(i)
            nums.append(0)
        else:
            i += 1
    return nums

if __name__ == '__main__':
    print(solve([3, 1, 0, 3,0, 12]))  # expected: [1, 3, 12, 0, 0]
