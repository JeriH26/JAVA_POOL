package training;

public class P010ClimbingStairs {
    // Time: O(n), Space: O(1)
    public static int solve(int n) {
        if (n <= 2) {
            return n;
        }
        int prev2 = 1;
        int prev1 = 2;
        for (int i = 3; i <= n; i++) {
            int next = prev1 + prev2;
            prev2 = prev1;
            prev1 = next;
        }
        return prev1;
    }

    public static void main(String[] args) {
        System.out.println(solve(2));
        System.out.println(solve(5));
    }
}
