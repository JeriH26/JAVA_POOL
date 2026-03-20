package training;

import java.util.HashMap;
import java.util.Map;

public class P001TwoSum {
    // Time: O(n), Space: O(n)
    public static int[] solve(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int need = target - nums[i];
            if (seen.containsKey(need)) {
                return new int[] {seen.get(need), i};
            }
            seen.put(nums[i], i);
        }
        return new int[] {};
    }

    public static void main(String[] args) {
        int[] ans = solve(new int[] {2, 7, 11, 15}, 9);
        System.out.println(ans[0] + "," + ans[1]);
    }
}
