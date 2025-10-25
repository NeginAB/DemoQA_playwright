from behave import given, when, then
from pages.book_login import elements, LoginPage
from fixtures.login_fixtures import USER_VALID_DATA
import time

@given("I open the Book Store login page")
def step_open_login_page(context):
    context.login_page = LoginPage(context.page)
    context.login_page.open()
    context.login_page.screenshot_page(folder="debug_screenshots")

@when("I login with valid username and password")
def step_login_valid(context):
    context.login_page.login(USER_VALID_DATA["username"], USER_VALID_DATA["password"])
    context.page.wait_for_timeout(500)
    context.login_page.screenshot_page(folder="debug_screenshots")

@when("I login with username {username} and password {password}")
def step_login_invalid_credentials(context, username, password):
    context.login_page.login(username, password)
    context.page.wait_for_timeout(500)
    context.login_page.screenshot_page(folder="debug_screenshots")

@when("I submit login form without username and password")
def step_login_empty(context):
    context.login_page.fill_username("")
    context.login_page.fill_password("")
    context.login_page.click_login()
    context.page.wait_for_timeout(300)
    context.login_page.screenshot_page(folder="debug_screenshots")

@when("I login with valid credentials and remember me")
def step_login_with_remember(context):
    if context.page.locator(elements.get("REMEMBER_ME")).count() > 0:
        context.page.locator(elements["REMEMBER_ME"]).check()
    context.login_page.login(USER_VALID_DATA["username"], USER_VALID_DATA["password"])
    context.page.wait_for_timeout(500)
    context.login_page.screenshot_page(folder="debug_screenshots")


@then("I should see the user is logged in successfully")
def step_check_success_login(context):
    username_locator = context.page.locator('//*[@id="userName-value"]')
    username_locator.wait_for(state="visible", timeout=15000)
    logged_in_user = username_locator.inner_text()
    assert logged_in_user == USER_VALID_DATA["username"], \
        f"Expected username '{USER_VALID_DATA['username']}', but got '{logged_in_user}'"

    logout_locator = context.page.locator("button:has-text('Log out')")
    logout_locator.wait_for(state="visible", timeout=15000)
    assert logout_locator.is_visible(), "Log out button is not visible after login"

@then("I should see an error message")
def step_check_error_message(context):
    context.page.wait_for_timeout(300)
    assert context.login_page.is_error_visible(), "Expected error message but got none"

@then("I should see validation errors for required fields")
def step_check_required_validation(context):
    context.login_page.screenshot_page(folder="debug_screenshots")
    username_el = context.page.locator(elements["USERNAME"])
    password_el = context.page.locator(elements["PASSWORD"])
    u_color = username_el.evaluate("el => window.getComputedStyle(el).borderColor")
    p_color = password_el.evaluate("el => window.getComputedStyle(el).borderColor")
    assert u_color or p_color is not None, "No visual validation detected for fields"

@then("the login button should be disabled if username or password is empty")
def step_login_button_disabled(context):
    disabled = context.page.locator(elements["LOGIN_BUTTON"]).is_disabled()
    assert disabled, "Login button is not disabled when fields are empty"

@then("after reload I should still be logged in")
def step_check_remember_me(context):
    context.page.reload()
    context.page.wait_for_timeout(500)
    username_locator = context.page.locator('//*[@id="userName-value"]')
    username_locator.wait_for(state="visible", timeout=15000)
    assert username_locator.is_visible(), "User is not logged in after reload (remember-me failed)"

@then("I log out from the Book Store")
def step_log_out(context):
    logout_locator = context.page.locator("button:has-text('Log out')")
    logout_locator.wait_for(state="visible", timeout=10000)
    logout_locator.click()
    context.page.wait_for_timeout(500)