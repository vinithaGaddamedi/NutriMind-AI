Feature: Integration Meal to Grocery
  As a backend system
  I want to accurately convert a meal plan into a grocery list
  So that users can buy exactly what they need

  Scenario: Generate grocery list from complex meal plan
    Given a complex weekly meal plan containing "Brown rice + dal + salad"
    When I submit the plan to the grocery engine
    Then the grocery list should contain "Brown rice" and "Dal"
    And the total cost should be calculated
