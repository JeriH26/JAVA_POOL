package training;

import java.util.Arrays;

public class P003MoveZeroes {
    // Time: O(n), Space: O(1)
    public static int[] solve(int[] nums) {
        int write = 0;
        for (int read = 0; read < nums.length; read++) {
            if (nums[read] != 0) {
                int tmp = nums[write];
                nums[write] = nums[read];
                nums[read] = tmp;
                write++;
            }
        }
        return nums;
    }

    public static void main(String[] args) {
        System.out.println(Arrays.toString(solve(new int[] {0, 1, 0, 3, 12})));
    }
}
