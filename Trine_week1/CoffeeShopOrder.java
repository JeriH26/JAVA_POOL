// Trine University Week 1 Java project: 
// You’ve been hired to create a simple Java program for a local coffee shop to calculate the total cost of an order. 
// The shop sells coffee, tea, and pastries, and they want to automatically calculate the total order cost, including tax.

package ordersystem;

public class CoffeeShopOrder {

    public static void main(String[] args) {

        // Number of the order
        int coffeesNumber = 2;
        int teasNumber = 1;
        int pastriesNumber = 3;

        // Prices of the order
        double coffeePrice = 3.50;
        double teaPrice = 2.75;
        double pastryPrice = 2.25;

        // Tax rate
        double taxRate = 0.07;

        // Calculate subtotal before tax
        double subtotal = (coffeesNumber * coffeePrice)
                        + (teasNumber * teaPrice)
                        + (pastriesNumber * pastryPrice);

        // Calculate tax amount and total cost
        double tax = subtotal * taxRate;
        double total = subtotal + tax;

        // Display results
        System.out.println("Coffees: " + coffeesNumber);
        System.out.println("Teas: " + teasNumber);
        System.out.println("Pastries: " + pastriesNumber);
        System.out.println("Subtotal: $" + String.format("%.2f", subtotal));
        System.out.println("Tax: $" + String.format("%.2f", tax));
        System.out.println("Total: $" + String.format("%.2f", total));

        // Comparison operator for a free drink
        if (total > 15) {
            System.out.println("You qualify for a free drink!");
        } else {
            System.out.println("Add more items to qualify for a free drink!");
        }
    }
}
