"""P006 Valid Parentheses Practice
TODO: implement solve(s)
"""


def solve(s):
    #raise NotImplementedError("TODO: implement p006 valid parentheses")
    #prev = None
    #while s != prev:
    #    prev = s
    #    s = s.replace("()", "").replace("[]", "").replace("{}", "")
    #return s == ""
    pair = {')':'(', ']':'[', '}':'{'}
    stack = []
    for ch in s:
        if ch in pair:
            if not stack or stack[-1] != pair[ch]:
                return False
            stack.pop()
        else:
            stack.append(ch)
    return len(stack) == 0





if __name__ == '__main__':
    print(solve('()[]{}'))  # expected: True
    print(solve('(]'))      # expected: False
