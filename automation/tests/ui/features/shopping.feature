Feature: NutriMind E2E Shopping Flow
  As a user
  I want to use the AI Meal Planner, check my Pantry, and checkout
  So that I can maintain a healthy diet

  Scenario: Generate meal plan and checkout using CSV data
    Given I log in with CSV user data
    When I generate a weekly meal plan
    And I check my pantry for available items
    And I add remaining groceries to the cart
    Then I successfully checkout and track my order
