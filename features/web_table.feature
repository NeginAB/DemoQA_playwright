Feature: Web Tables - CRUD operations

  Scenario: Add a new record
    Given I open the Web Tables page
    When I add a new record
    Then I should see the new record in the table

  Scenario: Update the first record
    Given I open the Web Tables page
    When I edit the first record
    Then I should see the updated data in the table

  Scenario: Delete the first record
    Given I open the Web Tables page
    When I delete the first record
    Then the record should no longer be in the table

  Scenario: Read and validate table data
    Given I open the Web Tables page
    When I read all table rows
    Then I should see the expected data in the table
