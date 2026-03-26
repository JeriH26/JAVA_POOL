"""P004 Container With Most Water Practice
TODO: implement solve(height)
"""


def solve(height):
    #raise NotImplementedError("TODO: implement p004 container with most water")
    #best = 0
    #left, right = 0, len(height)-1
    #while left < right:
    #    width = right - left
    #    area = min(height[left], height[right]) * width
    #    best = max(best, area)
    #    if height[left] < height[right]:
    #        left += 1
    #    else:
    #        right -=1
    #return best

    best = 0
    n = len(height)
    for i in range(n):
        for j in range(i+1, n):
            area = min(height[i], height[j]) * (j-i)
            best = max(best, area)
    return best


if __name__ == '__main__':
    print(solve([1, 8, 6, 2, 5, 4, 8, 3, 7]))  # expected: 49
