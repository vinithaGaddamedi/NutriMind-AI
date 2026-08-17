Feature: Nutrition Logic
  As a backend service
  I want to calculate accurate BMR and Macros
  So that users receive healthy meal plans

  Scenario Outline: Validate nutrition calculation based on goals
    Given a user profile with age "<age>", weight "<weight>", height "<height>", gender "<gender>", and goal "<goal>"
    When I request a meal plan
    Then the calculated calories should be around "<expected_calories>"
    And the protein ratio should match the goal

    Examples:
      | age | weight | height | gender | goal        | expected_calories |
      | 30  | 70     | 170    | female | weight_loss | 1100              |
      | 25  | 80     | 180    | male   | muscle_gain | 2100              |
      | 40  | 65     | 160    | female | maintenance | 1300              |
