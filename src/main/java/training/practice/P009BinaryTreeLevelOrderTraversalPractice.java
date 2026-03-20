package training.practice;

import java.util.List;

public class P009BinaryTreeLevelOrderTraversalPractice {
    static class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;

        TreeNode(int val) {
            this.val = val;
        }

        TreeNode(int val, TreeNode left, TreeNode right) {
            this.val = val;
            this.left = left;
            this.right = right;
        }
    }

    // TODO: return level order traversal result.
    public static List<List<Integer>> solve(TreeNode root) {
        throw new UnsupportedOperationException("TODO: implement P009BinaryTreeLevelOrderTraversalPractice.solve");
    }

    public static void main(String[] args) {
        TreeNode root = new TreeNode(3,
                new TreeNode(9),
                new TreeNode(20, new TreeNode(15), new TreeNode(7)));
        System.out.println(solve(root)); // expected: [[3], [9, 20], [15, 7]]
    }
}
