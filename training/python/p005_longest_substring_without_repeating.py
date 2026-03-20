"""P005 Longest Substring Without Repeating Characters
Time: O(n), Space: O(min(n, alphabet))
"""

def solve(s):
    left = 0
    best = 0
    index = {}
    for right, ch in enumerate(s):
        if ch in index and index[ch] >= left:
            left = index[ch] + 1
        index[ch] = right
        best = max(best, right - left + 1)
    return best


if __name__ == '__main__':
    print(solve('abcabcbb'))
    print(solve('bbbbb'))
