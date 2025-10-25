Feature: Book Store - Login (authentication flow)
  As a Book Store user
  I want to authenticate to the application
  So that I can access my account and books

  Background:
    Given I open the Book Store login page

  Scenario: Successful login with valid credentials
    When I login with valid username and password
    Then I should see the user is logged in successfully
    And I log out from the Book Store

  Scenario Outline: Unsuccessful login with invalid credentials
    When I login with username "<username>" and password "<password>"
    Then I should see an error message

    Examples:
      | username       | password        |
      | invalidUser    | wrongPassword  |
      | negin_test     | wrongPassword  |
      | wrongUser      | SecurePass123  |

  Scenario: Login with empty fields shows validation
    When I submit login form without username and password
    Then I should see validation errors for required fields

  Scenario: Login button should be disabled when fields are empty
    Then the login button should be disabled if username or password is empty

  Scenario: Login preserves session when "Remember Me" is enabled (if available)
    When I login with valid credentials and remember me
    Then after reload I should still be logged in
