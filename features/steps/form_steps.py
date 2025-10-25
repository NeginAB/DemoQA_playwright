from behave import given, when, then
from pages.form_page import FormPage, elements
import os
from fixtures.data_fixtures import STUDENT_VALID_DATA,STUDENT_LONG_ADDRESS,STUDENT_SPECIAL_NAME 
from playwright.sync_api import expect
from datetime import datetime



@given("I open the student registration form page")
def step_open_form(context):
    context.form_page = FormPage(context.page)
    context.form_page.open()


@when("I fill all required fields with valid information")
def step_fill_required_fields(context):
    context.form_page.fill_basic_info(
        first=STUDENT_VALID_DATA["first_name"],
        last=STUDENT_VALID_DATA["last_name"],
        email=STUDENT_VALID_DATA["email"],
        gender=STUDENT_VALID_DATA["gender"],
        mobile=STUDENT_VALID_DATA["mobile"]
    )

    context.form_page.page.locator(elements["DATE_OF_BIRTH"]).fill(STUDENT_VALID_DATA["date_of_birth"])
    for subject in STUDENT_VALID_DATA["subjects"]:
        context.form_page.page.locator(elements["SUBJECTS"]).fill(subject)
        context.form_page.page.keyboard.press("Enter")
    
    for hobby in STUDENT_VALID_DATA["hobbies"]:
        context.form_page.page.locator(elements[f"HOBBIES_{hobby.upper()}"]).click()
    context.form_page.page.locator(elements["CURRENT_ADDRESS"]).fill(STUDENT_VALID_DATA["current_address"])
    context.form_page.page.locator(elements["STATE"]).fill(STUDENT_VALID_DATA["state"])
    context.form_page.page.keyboard.press("Enter")
    context.form_page.page.locator(elements["CITY"]).fill(STUDENT_VALID_DATA["city"])
    context.form_page.page.keyboard.press("Enter")

@when("I submit the registration form")
def step_submit_form(context):
    context.form_page.submit_form()

@then("I should see a confirmation modal with success details")
def step_verify_success_modal(context):
    modal_data = context.form_page.get_confirmation_data()
    
    expected = {
        "Student Name": f"{STUDENT_VALID_DATA['first_name']} {STUDENT_VALID_DATA['last_name']}",
        "Student Email": STUDENT_VALID_DATA["email"],
        "Gender": STUDENT_VALID_DATA["gender"],
        "Mobile": STUDENT_VALID_DATA["mobile"],
        "Date of Birth": STUDENT_VALID_DATA["date_of_birth"],
        "Hobbies": ", ".join(STUDENT_VALID_DATA["hobbies"]),
        "Address": STUDENT_VALID_DATA["current_address"],
        "State and City": f"{STUDENT_VALID_DATA['state']} {STUDENT_VALID_DATA['city']}"
    }

    for key, value in expected.items():
        actual_value = modal_data.get(key, "")
        assert " ".join(actual_value.split()) == " ".join(value.split()), f"{key} mismatch: expected '{value}', got '{actual_value}'"

@when("I upload a valid image file")
def step_upload_valid_image(context):
    context.form_page.fill_basic_info(
        first=STUDENT_VALID_DATA["first_name"],
        last=STUDENT_VALID_DATA["last_name"],
        email=STUDENT_VALID_DATA["email"],
        gender=STUDENT_VALID_DATA["gender"],
        mobile=STUDENT_VALID_DATA["mobile"]
    )

    file_name = "khodro45.jpeg"
    file_path = os.path.abspath(f"features/fixtures/{file_name}")
    context.uploaded_file_name = file_name
    context.form_page.page.locator(elements["UPLOAD_PICTURE"]).set_input_files(file_path)
    context.form_page.submit_form()

@then("I should see the file name displayed in the success modal")
def step_verify_uploaded_file_in_modal(context):
    modal_locator = context.form_page.page.locator("#example-modal-sizes-title-lg")
    modal_locator.wait_for(state="visible", timeout=15000)
    modal_data = context.form_page.get_confirmation_data()
    uploaded_file_in_modal = modal_data.get("Picture", "")
    
    assert context.uploaded_file_name in uploaded_file_in_modal, \
        f"Uploaded file not displayed in modal: expected {context.uploaded_file_name}, got {uploaded_file_in_modal}"
    
@when("I select multiple hobbies")
def step_select_multiple_hobbies(context):
    hobbies_to_select = ["Sports", "Reading", "Music"]
    for hobby in hobbies_to_select:
        key = f"HOBBIES_{hobby.upper()}"
        if key in elements:
            element = context.form_page.page.locator(elements[key])
            element.scroll_into_view_if_needed()
            element.click()
    context.selected_hobbies = hobbies_to_select


@then("all selected hobbies should be visible as selected")
def step_verify_selected_hobbies(context):
    for hobby in getattr(context, "selected_hobbies", []):
        key = f"HOBBIES_{hobby.upper()}"
        element = context.form_page.page.locator(elements[key])
        assert element.is_checked(), f"Hobby '{hobby}' is not selected"
        

@when("I type part of a subject name and choose from suggestions")
def step_select_subject_from_suggestions(context):
    subject_partial = "ma"
    subject_full = "Maths"
    context.selected_subject = subject_full

    input_box = context.form_page.page.locator("#subjectsInput")
    input_box.fill(subject_partial)
    suggestion = context.form_page.page.locator(f"div[id^='react-select-2-option-']", has_text=subject_full)
    suggestion.wait_for(state="visible", timeout=5000)
    suggestion.click()


@then("the selected subject should appear in the input box")
def step_verify_selected_subject(context):
    selected_tag = context.form_page.page.locator(".subjects-auto-complete__multi-value__label")

    expect(selected_tag).to_have_text(context.selected_subject, timeout=5000)

    actual_subject = selected_tag.inner_text()
    assert context.selected_subject.lower() in actual_subject.lower(), \
        f"Expected subject '{context.selected_subject}' but got '{actual_subject}'"
    

@when("I select a valid state and city")
def step_select_state_city(context):
    context.form_page.fill_basic_info(
        first=STUDENT_VALID_DATA["first_name"],
        last=STUDENT_VALID_DATA["last_name"],
        email=STUDENT_VALID_DATA["email"],
        gender=STUDENT_VALID_DATA["gender"],
        mobile=STUDENT_VALID_DATA["mobile"]
    )
    context.form_page.page.locator("#state").click()
    state_option = context.form_page.page.locator("div[id^='react-select-3-option-']", has_text="NCR")
    state_option.wait_for(state="visible", timeout=5000)
    state_option.click()
    context.form_page.page.locator("#city").click()
    city_option = context.form_page.page.locator("div[id^='react-select-4-option-']", has_text="Delhi")
    city_option.wait_for(state="visible", timeout=5000)
    city_option.click()
    context.selected_state = "NCR"
    context.selected_city = "Delhi"
    context.form_page.page.locator(elements["SUBMIT_BUTTON"]).click()


@then("the selected state and city should be displayed in the success modal")
def step_verify_state_city_in_modal(context):
    modal_data = context.form_page.get_confirmation_data()
    expected = f"{STUDENT_VALID_DATA['state']} {STUDENT_VALID_DATA['city']}"
    actual_value = modal_data.get("State and City", "")
    actual_clean = " ".join(actual_value.split())
    
    assert actual_clean == expected, f"State and City mismatch: expected '{expected}', got '{actual_clean}'"



@when("I click submit without filling required fields")
def step_submit_empty_form(context):
    context.form_page.submit_form()

@then("I should see validation colors correctly for the form")
def step_check_validation_colors(context):
    context.form_page.submit_form()
    context.page.wait_for_timeout(500)

    required_fields = ["FIRST_NAME", "LAST_NAME", "MOBILE"]
    optional_fields = ["EMAIL", "DATE_OF_BIRTH", "CURRENT_ADDRESS"]

    for field in required_fields:
        is_red = context.form_page.is_field_red(field)  
        assert is_red, f"{field} should be red (empty required field)"

    for field in optional_fields:
        is_green = context.form_page.is_field_green(field)  
        assert is_green, f"{field} should be green (filled optional field)"


@when('I enter "{email}" as email')
def step_enter_email(context, email):
    context.form_page.page.locator(elements["EMAIL"]).fill(email)

@when("I click submit")
def step_click_submit(context):
    context.form_page.page.locator(elements["SUBMIT_BUTTON"]).click()


@then("I should see an error or invalid email indication")
def step_check_invalid_email(context):
    email_field = context.form_page.page.locator(elements["EMAIL"])
    
    context.page.wait_for_timeout(500)

    os.makedirs("screenshots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.abspath(f"screenshots/invalid_email_{timestamp}.png")
    email_field.screenshot(path=screenshot_path)
    print(f"[INFO] Screenshot saved: {screenshot_path}")
    border_color = email_field.evaluate("el => window.getComputedStyle(el).borderColor")
    error_detected = border_color.strip() == "rgb(220, 53, 69)"  

    assert error_detected, "Email field is not highlighted as invalid"

@when('I enter "{mobile}" in mobile number field')
def step_enter_mobile(context, mobile):
    context.form_page.page.locator(elements["MOBILE"]).fill(mobile)


@then("the mobile number field should reject invalid input")
def step_check_invalid_mobile(context):
    mobile_field = context.form_page.page.locator(elements["MOBILE"])
    
    context.page.wait_for_timeout(500)
    os.makedirs("screenshots", exist_ok=True)


    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.abspath(f"screenshots/invalid_mobile_{timestamp}.png")
    mobile_field.screenshot(path=screenshot_path)
    print(f"[INFO] Screenshot saved: {screenshot_path}")

    border_color = mobile_field.evaluate("el => window.getComputedStyle(el).borderColor")
    error_detected = border_color.strip() == "rgb(220, 53, 69)"  

    assert error_detected, "Mobile field is not highlighted as invalid"


@when('I upload a ".txt" file instead of an image')
def step_upload_invalid_file(context):
    context.form_page.fill_basic_info(
        first=STUDENT_VALID_DATA["first_name"],
        last=STUDENT_VALID_DATA["last_name"],
        email=STUDENT_VALID_DATA["email"],
        gender=STUDENT_VALID_DATA["gender"],
        mobile=STUDENT_VALID_DATA["mobile"]
    )
    file_name = "TaskA_Playwright_FINAL.txt"
    file_path = os.path.abspath(f"features/fixtures/{file_name}")
    context.uploaded_file_name = file_name
    context.form_page.page.locator(elements["UPLOAD_PICTURE"]).set_input_files(file_path)
    context.form_page.submit_form()  


@then("I should see an error or the upload should be ignored")
def step_check_invalid_upload(context):
    modal_locator = context.form_page.page.locator("#example-modal-sizes-title-lg")
    modal_locator.wait_for(state="visible", timeout=15000)
    modal_data = context.form_page.get_confirmation_data()
    uploaded_file_in_modal = modal_data.get("Picture", "")
    assert context.uploaded_file_name not in uploaded_file_in_modal, \
        f"Uploaded invalid file was displayed in modal: {uploaded_file_in_modal}"

@then("I should see all labels and placeholders with correct text")
def step_verify_labels(context):
    placeholders = {
        "FIRST_NAME": "First Name",
        "LAST_NAME": "Last Name",
        "EMAIL": "name@example.com",
        "MOBILE": "Mobile Number",
        "CURRENT_ADDRESS": "Current Address"
    }
    for field, placeholder in placeholders.items():
        actual = context.form_page.page.locator(elements[field]).get_attribute("placeholder")
        assert actual == placeholder, f"{field} placeholder mismatch: {actual}"

@when('I select "{gender1}" and then "{gender2}"')
def step_select_gender(context, gender1, gender2):
    context.form_page.page.locator(elements[f"GENDER_{gender1.upper()}"]).click()
    context.form_page.page.locator(elements[f"GENDER_{gender2.upper()}"]).click()

@then('only "{gender}" should remain selected')
def step_verify_selected_gender(context, gender):
    selected = context.form_page.page.locator(elements[f"GENDER_{gender.upper()}"])
    assert selected.is_checked(), f"{gender} is not selected"

@when("I open the date picker and select a valid date")
def step_select_date(context):
    context.form_page.page.locator(elements["DATE_OF_BIRTH"]).fill(STUDENT_VALID_DATA["date_of_birth"])

@then("the selected date should be displayed in the input box")
def step_verify_date(context):
    value = context.form_page.page.locator(elements["DATE_OF_BIRTH"]).input_value()
    assert value == STUDENT_VALID_DATA["date_of_birth"]

@when("I scroll to the bottom of the page")
def step_scroll_page(context):
    context.form_page.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")


@then("all elements should be visible and interactable")
def step_verify_scroll(context):
    for key, selector in elements.items():
        if key in ["SUCCESS_MODAL", "CLOSE_MODAL"]:
            continue  
        element = context.form_page.page.locator(selector)
        assert element.is_visible(), f"{key} not visible"


@then("the confirmation modal should display the same information I entered")
def step_verify_modal_data(context):
    modal_text = context.form_page.get_success_message()
    for value in [STUDENT_VALID_DATA["first_name"], STUDENT_VALID_DATA["last_name"], STUDENT_VALID_DATA["email"]]:
        assert value in modal_text, f"{value} not found in modal"

@when('I fill the form with "{gender}" as gender')
def step_fill_with_gender(context, gender):
    context.form_page.fill_basic_info(
        first=STUDENT_VALID_DATA["first_name"],
        last=STUDENT_VALID_DATA["last_name"],
        email=STUDENT_VALID_DATA["email"],
        gender=gender,
        mobile=STUDENT_VALID_DATA["mobile"]
    )

@then("all fields should be cleared after closing the success modal")
def step_verify_reset(context):
    context.form_page.page.locator(elements["CLOSE_MODAL"]).click()
    for key in ["FIRST_NAME","LAST_NAME","EMAIL","MOBILE","CURRENT_ADDRESS"]:
        value = context.form_page.page.locator(elements[key]).input_value()
        assert value == "", f"{key} not cleared"

@then("I should see success modal")
def step_check_success_modal(context):
    success_modal = context.form_page.page.locator(elements["SUCCESS_MODAL"])
    try:
        success_modal.wait_for(state="visible", timeout=3000)
        visible = True
    except TimeoutError:
        visible = False
    print(f"Success modal visible: {visible}")

@when("I fill and submit the form")
def step_fill_and_submit_form(context):
    context.form_page.fill_basic_info(
        first=STUDENT_VALID_DATA["first_name"],
        last=STUDENT_VALID_DATA["last_name"],
        email=STUDENT_VALID_DATA["email"],
        gender=STUDENT_VALID_DATA["gender"],
        mobile=STUDENT_VALID_DATA["mobile"]
    )

 
    context.form_page.page.locator(elements["DATE_OF_BIRTH"]).fill(STUDENT_VALID_DATA["date_of_birth"])

    for subject in STUDENT_VALID_DATA["subjects"]:
        subj_input = context.form_page.page.locator(elements["SUBJECTS"])
        subj_input.fill(subject)
        context.form_page.page.keyboard.press("Enter")
        context.selected_subject = subject

    context.selected_hobbies = STUDENT_VALID_DATA["hobbies"]
    for hobby in context.selected_hobbies:
        context.form_page.page.locator(elements[f"HOBBIES_{hobby.upper()}"]).click()
    context.form_page.page.locator(elements["CURRENT_ADDRESS"]).fill(STUDENT_VALID_DATA["current_address"])
    context.form_page.page.locator(elements["STATE"]).fill(STUDENT_VALID_DATA["state"])
    context.form_page.page.keyboard.press("Enter")
    context.form_page.page.locator(elements["CITY"]).fill(STUDENT_VALID_DATA["city"])
    context.form_page.page.keyboard.press("Enter")

    if hasattr(context, "uploaded_file_name"):
        file_path = os.path.abspath(f"features/fixtures/{context.uploaded_file_name}")
        context.form_page.page.locator(elements["UPLOAD_PICTURE"]).set_input_files(file_path)

    context.form_page.page.locator(elements["SUBMIT_BUTTON"]).click()


@when("I enter a 200-character long address")
def step_long_address(context):
    context.form_page.page.locator(elements["CURRENT_ADDRESS"]).fill(STUDENT_LONG_ADDRESS)

@then("the input should accept all characters and not overflow")
def step_verify_long_address(context):
    value = context.form_page.page.locator(elements["CURRENT_ADDRESS"]).input_value()
    assert len(value) == 200

@when('I enter "@Negin!" as first name')
def step_special_char_first_name(context):
    context.form_page.page.locator(elements["FIRST_NAME"]).fill(STUDENT_SPECIAL_NAME)
    context.form_page.page.locator(elements["SUBMIT_BUTTON"]).click()


@then("the field should reject invalid input visually")
def step_reject_if_green(context):
    first_name_field = context.form_page.page.locator(elements["FIRST_NAME"])
    os.makedirs("screenshots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.abspath(f"screenshots/first_name_{timestamp}.png")
    first_name_field.screenshot(path=screenshot_path)
    print(f"[INFO] Screenshot saved: {screenshot_path}")
    border_color = first_name_field.evaluate("el => window.getComputedStyle(el).borderColor").strip()
    is_green = border_color == "rgb(40, 167, 69)"  
    assert not is_green, "Field is green but it should reject invalid input"



