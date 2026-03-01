package ShopSmartRewardSys;
// This project is developed by Junyi Huang, a student enrolled in the MSIS program at the Trine University.
/*  Week 4 Project: Given that I've been hired as a junior software developer for ShopSmart Retail, a company 
    that provides e-commerce solutions for small businesses.
    The company is building a new Customer Rewards System that calculates reward points based on customer type 
    and purchase amount. To make the system flexible, 
    your team uses interfaces, enums, sealed classes, and lambdas to simplify and streamline business logic.
*/ 

// ShopSmartRewardSys.java
import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;

// Interface for reward calculation， defining a contract for Reward customers
interface Rewardable {
    double calculatePoints(double purchaseAmount);
}

// Enum for customer types， defining different categories
enum CustomerType {
    REGULAR, PREMIUM
}

// Sealed class for customers， allowing only specific subclasses
sealed class Customer permits RegularCustomer, PremiumCustomer {
    String name;
    CustomerType type;

    Customer(String name, CustomerType type) {
        this.name = name;
        this.type = type;
    }
}

// Regular customer class implementing reward calculation
final class RegularCustomer extends Customer implements Rewardable {
    // Constructor, setting customer type to REGULAR
    RegularCustomer(String name) {
        super(name, CustomerType.REGULAR);
    }

    // Regular customers earn 1 point per dollar spent
    public double calculatePoints(double purchaseAmount) {
        return purchaseAmount * 1.0;
    }
}

// Premium customer class implementing reward calculation 
final class PremiumCustomer extends Customer implements Rewardable {
    // Constructor, setting customer type to PREMIUM
    PremiumCustomer(String name) {
        super(name, CustomerType.PREMIUM);
    }

    // Premium customers earn 1.5 points per dollar spent
    public double calculatePoints(double purchaseAmount) {
        return purchaseAmount * 1.5;
    }
}

// Main class for the ShopSmart Rewards System
public class ShopSmartRewardSys {

    public static void main(String[] args) {
        double purchaseAmount = 200.00;

        // Create a list of customers
        List<Customer> customers = new ArrayList<>();
        customers.add(new RegularCustomer("Maria Lopez"));
        customers.add(new PremiumCustomer("David Chen"));

        // Lambda for seasonal bonus calculation， adding 10% bonus points to the calculated points
        Function<Double, Double> bonus = points -> points * 1.10;

        // Calculate and display reward points for each customer
        for (Customer c : customers) {
            Rewardable r = (Rewardable) c;
            double basePoints = r.calculatePoints(purchaseAmount);
            double finalPoints = bonus.apply(basePoints);

            System.out.println("\n"); // Newline for readability

            // Display customer info and points
            System.out.println("Customer: " + c.name);
            System.out.println("Type: " + c.type);
            System.out.printf("Purchase: $%.2f%n", purchaseAmount);
            System.out.printf("Base Points: %.0f%n", basePoints);
            System.out.println("Bonus Applied: 10%");
            System.out.printf("Final Points: %.1f%n", finalPoints);
            System.out.println("\n"); // Newline for readability
        }
    }
}


/*
    Reflection Questions    

        1) How does polymorphism make this system easier to expand for new customer types (e.g., Corporate, Student)?   

            Polymorphism helps because the main code does not need to know the exact customer class.
            In the loop, I treat each customer as Reward and just call calculatePoints().
            If I add a new type like CorporateCustomer, I can create a new class that implements Reward
            and provides its own calculatePoints() rule. Then I can add it to the list, and the loop can stay the same. 

        2) Why might a company want to use sealed classes in a production environment?  

            A sealed class lets the company control which subclasses are allowed.
            In this project, Customer can only be RegularCustomer or PremiumCustomer.
            This is useful in production because it prevents someone from creating an unapproved customer type
            that could break the reward rules or cause unexpected behavior. It keeps the system safer and more predictable. 

        3) How do lambdas help reduce repetitive code in business applications? 

            The bonus rule (like 10% seasonal bonus) is the same for all customers.
            Instead of writing the same multiplication code many times, I store it as a lambda function.
            Then I can apply it to any points value in one line. If the bonus changes, I only update the lambda
            in one place, which makes the code cleaner and easier to maintain.
*/

