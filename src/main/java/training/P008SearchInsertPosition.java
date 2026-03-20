package training;

public class P008SearchInsertPosition {
    // Time: O(log n), Space: O(1)
    public static int solve(int[] nums, int target) {
        int left = 0;
        int right = nums.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) {
                return mid;
            }
            if (nums[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return left;
    }

    public static void main(String[] args) {
        System.out.println(solve(new int[] {1, 3, 5, 6}, 5));
        System.out.println(solve(new int[] {1, 3, 5, 6}, 2));
    }
}
