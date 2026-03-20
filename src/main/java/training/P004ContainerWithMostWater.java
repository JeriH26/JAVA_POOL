package training;

public class P004ContainerWithMostWater {
    // Time: O(n), Space: O(1)
    public static int solve(int[] height) {
        int left = 0;
        int right = height.length - 1;
        int best = 0;
        while (left < right) {
            int width = right - left;
            int area = Math.min(height[left], height[right]) * width;
            best = Math.max(best, area);
            if (height[left] < height[right]) {
                left++;
            } else {
                right--;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(solve(new int[] {1, 8, 6, 2, 5, 4, 8, 3, 7}));
    }
}
