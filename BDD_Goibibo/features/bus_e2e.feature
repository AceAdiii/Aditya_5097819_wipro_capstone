@bus @booking @e2e @regression
Feature: Goibibo bus booking end to end

  @smoke @payment @critical
  Scenario: Complete bus booking journey until card payment page
    Given the Goibibo bus module is open
    When I search buses from "Delhi" to "Lucknow"
    Then bus search results should be displayed
    When I choose a bus and open seat selection
    And I select boarding point, dropping point, and one available seat
    And I continue to traveller details
    And I skip travel insurance
    And I enter passenger details
      | name          | age | email            | mobile     | address     | pincode |
      | Aditya Pandey | 23  | aditya@gmail.com | 9876543210 | Patna Bihar | 800001  |
    And I confirm billing details and choose personal trip
    And I proceed to payment
    And I select card payment option
    Then the card payment page should be displayed

