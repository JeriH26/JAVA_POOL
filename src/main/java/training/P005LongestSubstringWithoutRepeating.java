package training;

import java.util.HashMap;
import java.util.Map;

public class P005LongestSubstringWithoutRepeating {
    // Time: O(n), Space: O(min(n, alphabet))
    public static int solve(String s) {
        int left = 0;
        int best = 0;
        Map<Character, Integer> index = new HashMap<>();
        for (int right = 0; right < s.length(); right++) {
            char ch = s.charAt(right);
            if (index.containsKey(ch) && index.get(ch) >= left) {
                left = index.get(ch) + 1;
            }
            index.put(ch, right);
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        System.out.println(solve("abcabcbb"));
        System.out.println(solve("bbbbb"));
    }
}
