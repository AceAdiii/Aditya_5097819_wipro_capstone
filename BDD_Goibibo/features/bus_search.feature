@bus @search @regression
Feature: Goibibo bus search module

  Background:
    Given the Goibibo bus module is open

  @smoke @positive @tc_p01
  Scenario: TC-P01 Search buses with valid source and destination
    When I search buses from "Delhi" to "Lucknow"
    Then bus search results should be displayed

  @positive @filter @ac @tc_p02
  Scenario: TC-P02 Apply AC filter on bus search results
    When I search buses from "Delhi" to "Lucknow"
    And I apply the AC bus filter
    Then bus search results should be displayed

  @positive @filter @sleeper @tc_p03
  Scenario: TC-P03 Apply Sleeper filter on bus search results
    When I search buses from "Delhi" to "Lucknow"
    And I apply the Sleeper bus filter
    Then bus search results should be displayed

  @positive @sort @price @tc_p04
  Scenario: TC-P04 Sort bus search results by price
    When I search buses from "Delhi" to "Lucknow"
    And I sort the bus results by price
    Then bus results should be sorted by lowest price first

  @positive @sort @duration @tc_p05
  Scenario: TC-P05 Sort bus search results by duration
    When I search buses from "Delhi" to "Lucknow"
    And I sort the bus results by duration
    Then bus results should be sorted by shortest duration first

  @negative @validation @tc_n01
  Scenario: TC-N01 Search with same source and destination city
    When I enter bus source "Delhi" and destination "Delhi"
    And I click the Search Bus button
    Then the same-city validation message should be displayed

  @negative @validation @tc_n02
  Scenario: TC-N02 Search with empty source city
    When I leave the bus source empty
    And I enter bus destination "Lucknow"
    And I click the Search Bus button
    Then bus search results should not be displayed
