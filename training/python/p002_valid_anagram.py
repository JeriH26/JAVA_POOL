"""P002 Valid Anagram
Time: O(n), Space: O(1) for fixed alphabet
"""


def solve(s, t):
    if len(s) != len(t):
        return False
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    for ch in t:
        if ch not in freq:
            return False
        freq[ch] -= 1
        if freq[ch] < 0:
            return False
    return True


if __name__ == '__main__':
    print(solve('anagram', 'nagaram'))
    print(solve('rat', 'car'))
