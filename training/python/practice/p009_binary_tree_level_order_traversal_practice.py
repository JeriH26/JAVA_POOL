"""P009 Binary Tree Level Order Traversal Practice
TODO: implement solve(root)
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def solve(root):
    raise NotImplementedError("TODO: implement p009 level order traversal")


if __name__ == '__main__':
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20, TreeNode(15), TreeNode(7))
    print(solve(root))  # expected: [[3], [9, 20], [15, 7]]
