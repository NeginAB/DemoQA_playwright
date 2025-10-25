Feature: Student Registration Form

Background:
    Given I open the student registration form page

  Scenario: Successfully submit the form with valid data
    When I fill all required fields with valid information
    And I submit the registration form
    Then I should see a confirmation modal with success details

  Scenario: Successfully upload a profile picture
    When I upload a valid image file
    Then I should see the file name displayed in the success modal

  Scenario: Successfully select multiple hobbies
    When I select multiple hobbies
    Then all selected hobbies should be visible as selected

  Scenario: Successfully select a subject using auto-suggestion
    When I type part of a subject name and choose from suggestions
    Then the selected subject should appear in the input box

  Scenario: Successfully choose state and city
    When I select a valid state and city
    Then the selected state and city should be displayed in the success modal

  Scenario: Try to submit the form with empty required fields
    When I click submit without filling required fields
    Then I should see validation colors correctly for the form

  Scenario: Enter invalid email format
    When I enter "negin@" as email
    And I click submit
    Then I should see an error or invalid email indication

  Scenario: Enter non-numeric value in mobile number
    When I enter "abc123" in mobile number field
    And I click submit
    Then the mobile number field should reject invalid input

  Scenario: Upload invalid file type as picture
    When I upload a ".txt" file instead of an image
    Then I should see an error or the upload should be ignored

  Scenario: Verify all field labels and placeholders are displayed correctly
    Then I should see all labels and placeholders with correct text

  Scenario: Verify gender radio buttons are selectable one at a time
    When I select "Male" and then "Female"
    Then only "Female" should remain selected

  Scenario: Verify date picker allows selecting a valid date
    When I open the date picker and select a valid date
    Then the selected date should be displayed in the input box

  Scenario: Verify scrolling and responsiveness of form
    When I scroll to the bottom of the page
    Then all elements should be visible and interactable

  Scenario: Verify form can be submitted with different gender options
    When I fill the form with "Male" as gender
    And I submit the registration form
    Then I should see success modal

  Scenario: Verify form reset after submission
    When I fill and submit the form
    Then all fields should be cleared after closing the success modal

  Scenario: Enter long text in address field
    When I enter a 200-character long address
    Then the input should accept all characters and not overflow

  Scenario: Enter special characters in name fields
    When I enter "@Negin!" as first name
    Then the field should reject invalid input visually
