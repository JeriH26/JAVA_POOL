package training;

import java.util.Arrays;

public class Runner {
    public static void main(String[] args) {
        System.out.println("P001 Two Sum: " + Arrays.toString(P001TwoSum.solve(new int[] {2, 7, 11, 15}, 9)));
        System.out.println("P004 Container: " + P004ContainerWithMostWater.solve(new int[] {1, 8, 6, 2, 5, 4, 8, 3, 7}));
        System.out.println("P006 Parentheses: " + P006ValidParentheses.solve("()[]{}"));
        System.out.println("P010 Climbing Stairs: " + P010ClimbingStairs.solve(5));
    }
}
