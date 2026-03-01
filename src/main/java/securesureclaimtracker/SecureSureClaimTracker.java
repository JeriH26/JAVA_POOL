package securesureclaimtracker;

/*
This project is an acacdemic exercise from Trine University, made by Junyi Huang, 
for the course "Programming Fundamentals in Java". 
Given I’ve joined the software development team at SecureSure Insurance, 
a national company that manages thousands of customer claims each month. 
The Claims Department wants to modernize how it tracks workflow activity during the day.

The project is a simple GUI application that tracks insurance claims. 
It allows users to add claims, view the total number of claims processed, 
and reset the count. Each claim is logged in an ArrayList, 
and a milestone message is displayed when 10 claims are reached.
 */

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;

public class SecureSureClaimTracker extends JFrame {

    // Variable to track total claims
    private int claimCount = 0;

    // ArrayList to store log entries (simulating a log)
    private ArrayList<Integer> claimLog = new ArrayList<Integer>();

    // GUI components
    private JLabel countLabel;
    private JTextArea logArea;
    private JLabel milestoneLabel;

    public SecureSureClaimTracker() {
        super("SecureSure Claim Tracker"); // required window title
        buildUI(); // method to set up the user interface
    }

    private void buildUI() {
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // close app on exit
        setSize(420, 300); // fixed size for simplicity
        setLocationRelativeTo(null); // center on screen

        // Main panel with BorderLayout
        JPanel mainPanel = new JPanel();
        mainPanel.setLayout(new BorderLayout(10, 10));
        mainPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // Top: count label + milestone label
        JPanel topPanel = new JPanel();
        topPanel.setLayout(new GridLayout(2, 1));

        countLabel = new JLabel("Claims Processed: 0"); // initial text
        countLabel.setFont(new Font("SansSerif", Font.BOLD, 18)); // larger font for visibility

        milestoneLabel = new JLabel(" "); // empty by default

        topPanel.add(countLabel); // add count label to top panel
        topPanel.add(milestoneLabel); // add milestone label to top panel

        // Center: log area with scroll pane
        logArea = new JTextArea();
        logArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(logArea);

        // Bottom: buttons with FlowLayout
        JButton addButton = new JButton("Add Claim");
        JButton resetButton = new JButton("Reset");

        // ActionListener for Add Claim button
        addButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                addClaim();
            }
        });

        // ActionListener for Reset button
        resetButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                resetClaims();
            }
        });

        JPanel bottomPanel = new JPanel(); // panel for buttons
        bottomPanel.setLayout(new FlowLayout(FlowLayout.CENTER, 10, 5)); // center buttons with spacing
        bottomPanel.add(addButton); // add "Add Claim" button to bottom panel
        bottomPanel.add(resetButton); // add "Reset" button to bottom panel

        // Assemble main panel with top, center, and bottom sections
        mainPanel.add(topPanel, BorderLayout.NORTH);
        mainPanel.add(scrollPane, BorderLayout.CENTER);
        mainPanel.add(bottomPanel, BorderLayout.SOUTH);

        add(mainPanel);
        setVisible(true);
    }

    // add a claim, update count, log, and display
    private void addClaim() {
        // Update variable
        claimCount++;

        // Store log entry in ArrayList
        claimLog.add(claimCount);

        // Update UI
        updateDisplay();

        // Conditional milestone message and label update
        if (claimCount == 10) {
            JOptionPane.showMessageDialog(
                    this,
                    "Congratulations! You've logged 10 claims.",
                    "Milestone",
                    JOptionPane.INFORMATION_MESSAGE
            );
            milestoneLabel.setText("Milestone reached: 10 claims!"); // update milestone label
        } else {
            milestoneLabel.setText(" ");
        }
    }

    // reset everything to initial state
    private void resetClaims() {
        claimCount = 0;
        claimLog.clear();
        milestoneLabel.setText(" ");
        updateDisplay();
    }

    // update label + log area
    private void updateDisplay() {
        countLabel.setText("Claims Processed: " + claimCount);

        // Loop through ArrayList and display
        String logText = "";
        for (int i = 0; i < claimLog.size(); i++) {
            logText = logText + "Log Entry " + (i + 1) + ": Claims Processed = " + claimLog.get(i) + "\n";
        }
        logArea.setText(logText);
    }

    // Main method on EDT
    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                new SecureSureClaimTracker();
            }
        });
    }
}
