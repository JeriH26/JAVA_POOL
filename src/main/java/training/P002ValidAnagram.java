package training;

public class P002ValidAnagram {
    // Time: O(n), Space: O(1) for fixed alphabet
    public static boolean solve(String s, String t) {
        if (s.length() != t.length()) {
            return false;
        }
        int[] freq = new int[26];
        for (int i = 0; i < s.length(); i++) {
            freq[s.charAt(i) - 'a']++;
            freq[t.charAt(i) - 'a']--;
        }
        for (int v : freq) {
            if (v != 0) {
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        System.out.println(solve("anagram", "nagaram"));
        System.out.println(solve("rat", "car"));
    }
}
