// This is the academic Java code file asked by Trine University for Week 2 project:
// RewardsTracker.java
/*  a simple Java program that processes a list of customer purchases, calculates the total spending, 
    determines the appropriate rewards tier, and applies bonus points for special promotions.
*/

package creditcardpro;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

public class RewardsTracker {

    public static void main(String[] args) {

        // Set arrays of categories + transaction ShopAmounts + promo code
        String[] ShopCategories = {"GROCERY", "DINING", "TRAVEL", "GAS", "OTHER"};
        double[] ShopAmounts = {125.40, 63.15, 327.00, 45.30, 26.00}; // try some inputdata set to reach total 586.85
        String promoCode = new String("BONUS10");

        // Use a loop to calculate total amount
        double TotalSpentAmt = 0.0;
        for (double amtNumber : ShopAmounts) {
            TotalSpentAmt += amtNumber;
        }

        // Use math to round to two decimal
        TotalSpentAmt = Math.round(TotalSpentAmt * 100.0) / 100.0;

        String tierName;
        int tierProduct;
        // if-else for tiers based on total spent amount
        if (TotalSpentAmt >= 500.0) {
            tierName = "Platinum";
            tierProduct = 3;
        } else if (TotalSpentAmt >= 250.0) {
            tierName = "Gold";
            tierProduct = 2;
        } else {
            tierName = "Silver";
            tierProduct = 1;
        }

        // Given base points is like 1 point per $1, then apply tier product to be a round int
        int basePoints = (int) Math.round(TotalSpentAmt) * tierProduct;
        String promoNormalized = promoCode.toUpperCase();
        double bonusRate;

        // switch statement for promo codes
        switch (promoNormalized) {
            case "BONUS10":
                bonusRate = 0.10;
                break;
            case "TRAVEL5":
                bonusRate = 0.05;
                break;
            default:
                bonusRate = 0.0;
        }

        // Calculate bonus points and total points
        int bonusPoints = (int) Math.round(basePoints * bonusRate);
        int totalPoints = basePoints + bonusPoints;

        // Output equality demo:
        System.out.println("Equality demo:\n");
        // Set == compares whether both variables point to the exact same object
        System.out.println(promoCode == "BONUS10");
        // Set .equals() to compare the actual text content, regardless of whether they are the same object
        System.out.println(promoCode.equals("BONUS10"));

        // Use while loop to progress message a few times
        System.out.println("\n");
        int i = 0;
        while (i < 3) {
            System.out.println("Calculating rewards...");
            i++;
        }

        // Dates --> java.time
        LocalDate today = LocalDate.now();
        LocalDate nextBilling = today.plusDays(30);

        // Format dates to string
        DateTimeFormatter defineFmt = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        String todayStr = today.format(defineFmt);
        String nextBillingStr = nextBilling.format(defineFmt);

        // StringBuilder for formatted output
        StringBuilder SBToOutput = new StringBuilder();
        SBToOutput.append("\n\n=== CreditCardPro Monthly Summary ===\n\n");
        SBToOutput.append("Date: ").append(todayStr).append("\n");
        SBToOutput.append("Next Billing: ").append(nextBillingStr).append("\n");
        SBToOutput.append("------------------------------\n");
        // Formatted output with two decimal places for dollar amount
        SBToOutput.append(String.format("Total Spending: $%.2f%n%n", TotalSpentAmt));
        // Tier and points output
        SBToOutput.append("Tier: ").append(tierName).append(" (x").append(tierProduct).append(" points)\n");
        SBToOutput.append("Base Points: ").append(basePoints).append("\n");
        SBToOutput.append("Bonus Points: ").append(bonusPoints).append("\n");
        SBToOutput.append("Total Points Earned: ").append(totalPoints).append("\n");
        SBToOutput.append("Promo Code: ").append(promoNormalized).append("\n");
        SBToOutput.append("Message: Great work! Keep building your rewards.\n");

        System.out.print(SBToOutput);
    }
}
