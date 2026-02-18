/*  This is an academic project assigned by Trine University for OOP in Java, developed by Junyi Huang.

    Given I am a new developer at GlobalPay Financial Services, 
    a company that helps small businesses process international payments.
    My manager has asked to build a simple currency converter program that shows 
    how the company might display clear, user-friendly error messages and organize its code into a modular structure.

    The program should accept an amount in U.S. dollars, convert it to another currency, and handle any invalid input gracefully.
 */
// module-info.java
package globalpay.converter;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;
import java.util.MissingResourceException;
import java.util.PropertyResourceBundle;
import java.util.ResourceBundle;
import java.util.Scanner;

// CurrencyConverter.java
public class CurrencyConverter {

    // Exchange rates (for simplicity, these are hardcoded)
    private static final double USD_TO_EUR = 0.90;
    private static final double USD_TO_MXN = 17.00;

    public static void main(String[] args) {

        // Load messages from the resource bundle
        ResourceBundle messages = loadMessages();

        // Use try-with-resources to ensure the scanner is closed properly
        try (Scanner scanner = new Scanner(System.in)) {
            // Display welcome message
            System.out.println(messages.getString("welcome"));

            // Prompt user for amount and handle invalid input
            double amount;
            try {
                System.out.println(messages.getString("enterAmount"));
                amount = Double.parseDouble(scanner.nextLine()); // Read the entire line to avoid issues with nextDouble() and newline characters
            } catch (NumberFormatException e) {
                // If the input is not a valid number, display an error message and exit
                System.out.println(messages.getString("errorInvalid"));
                System.out.println(messages.getString("thankYou"));
                return;
            }

            // Prompt user for target currency
            System.out.println(messages.getString("enterCurrency"));
            String currency = scanner.nextLine().toUpperCase(); // Convert input to uppercase for case-insensitive comparison

            double converted;

            // Perform currency conversion based on user input
            if (currency.equals("EUR")) {
                // Calculate the converted amount and display the result from US to Euros
                converted = amount * USD_TO_EUR;
                System.out.printf("%s €%.2f%n", messages.getString("result"), converted);

            } else if (currency.equals("MXN")) {
                // Calculate the converted amount and display the result from US to Mexican Pesos
                converted = amount * USD_TO_MXN;
                System.out.printf("%s %.2f MXN%n", messages.getString("result"), converted);

            } else {
                // If the user enters an unsupported currency, display an error message and exit
                System.out.println(messages.getString("errorCurrency"));
                System.out.println(messages.getString("thankYou"));
                return;
            }

            // Display thank you message after successful conversion
            System.out.println(messages.getString("thankYou"));
        }
    }

    /* I didn't explain this following part in the video, because this is bug fix part for Messages_en_US.properties path, 
    as I put it in the path of src/main/resources, Java is hard to read this file. That why I fix additionally*/

    // Method to load messages from the resource bundle, with a fallback to a file if the bundle is missing
    private static ResourceBundle loadMessages() {
        try {
            // Attempt to load the resource bundle from the classpath
            return ResourceBundle.getBundle("Messages", Locale.US);
        } catch (MissingResourceException e) {
            // If the resource bundle is not found in the classpath, attempt to load it from a fallback file
            Path fallback = Path.of("src/main/resources/Messages_en_US.properties");
            try (InputStream in = Files.newInputStream(fallback)) {
                return new PropertyResourceBundle(in); // Load the properties file directly from the specified path
            } catch (IOException ioException) {
                // If the fallback file also cannot be loaded, throw an exception with a clear message
                throw new IllegalStateException("Cannot load messages bundle from classpath or " + fallback, ioException);
            }
        }
    }
}
