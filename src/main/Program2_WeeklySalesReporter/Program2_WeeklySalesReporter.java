package Program2_WeeklySalesReporter;
/*
    Name: Junyi Huang
    Course: Object-Oriented Programming in Java
    Program: Program2_WeeklySalesReporter

    Given that I've been hired as a junior developer at RetailIQ Analytics, 
    a company that creates business dashboards for small retail stores.
    This is a simple Java program that displays weekly sales performance data for one of your store clients. 
    The program will list 10 daily sales totals, calculate the weekly average, and display the store name at the top of the report.
 */

// Program2_WeeklySalesReporter.java
public class Program2_WeeklySalesReporter {

    // Calculates the average sales value from the array of daily sales.
    public static double calculateAverage(double[] sales) {
        double total = 0.0;

        // Sum up all the sales values
        for (double value : sales) {
            total += value;
        }

        // Calculate the average by dividing the total by the number of sales entries
        double average = total / sales.length;

        return average;
    }

    public static void main(String[] args) {

        // Store name for the report
        String storeName = "Trendy Threads Boutique";

        // Array holding 10 daily sales totals
        double[] dailySales = {
            1200.50, 985.25, 1105.75, 1340.00, 1015.30,
            970.45, 1500.00, 880.50, 1120.75, 995.00
        };

        // Display the store name
        System.out.println("Store: " + storeName);

        // Display the daily sales totals
        System.out.print("Daily Sales: ");
        for (int i = 0; i < dailySales.length; i++) {
            System.out.printf("%.2f", dailySales[i]); // Format each sales value to two decimal places
            if (i < dailySales.length - 1) {
                System.out.print(", "); // Add a comma and space between sales values, but not after the last one
            }
        }
        System.out.println(); // Move to the next line after displaying daily sales

        // Calculate average sales
        double averageSales = calculateAverage(dailySales);

        // Display average sales formatted to two decimal places
        System.out.printf("Average Daily Sales: $%.2f%n", averageSales);
    }
}

