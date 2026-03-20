"""P002 Valid Anagram Practice
TODO: implement solve(s, t)
"""


def solve(s, t):
    #if len(s) != len(t):
    #    return False
    #
    #freq = {}
    #for ch in s:
    #    freq[ch] = freq.get(ch, 0) + 1
    #for ch in t:
    #    if ch not in freq:
    #        return False
    #    freq[ch] -=1
    #    if freq[ch] < 0:
    #        return False
    #return True

    if len(s) != len(t):
        return False
    
    t_list = list(t)
    for ch in s:
        if ch in t_list:
            t_list.remove(ch)
        else:
            return False
    return True

if __name__ == '__main__':
    print(solve('anagram', 'nagaram'))  # expected: True
    print(solve('rat', 'car'))          # expected: False
