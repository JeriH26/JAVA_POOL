"""P005 Longest Substring Without Repeating Practice
TODO: implement solve(s)
"""


def solve(s):
    #raise NotImplementedError("TODO: implement p005 longest substring")

    #n = len(s)
    #best = 0
    #for i in range(n):
    #    seen = set()
    #    for j in range(i, n):
    #        if s[j] in seen:
    #            break
    #        seen.add(s[j])
    #        best = max(best, j-i+1)
    #return best

    #n = len(s)
    #best = 0
    #for i in range(n):
    #    for j in range(i+1, n):
    #        sub = s[i:j]
    #        if len(set(sub)) == len(sub):
    #            best = max(best, len(sub))
    #return best

    left = 0
    index = {}
    best = 0
    for right, ch in enumerate(s):
        if ch in index and index[ch] >= left:
            left = index[ch] +1
        index[ch] = right
        best = max(best, right-left+1)
    return best


if __name__ == '__main__':
    print(solve('abcabcbb'))  # expected: 3
    print(solve('bbbbb'))     # expected: 1
