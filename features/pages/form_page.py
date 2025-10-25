from playwright.sync_api import Page
import os
elements = {
    "FIRST_NAME": "#firstName",
    "LAST_NAME": "#lastName",
    "EMAIL": "#userEmail",
    "GENDER_MALE": "//label[text()='Male']",
    "GENDER_FEMALE": "//label[text()='Female']",
    "GENDER_OTHER": "//label[text()='Other']",
    "MOBILE": "#userNumber",
    "DATE_OF_BIRTH": "#dateOfBirthInput",
    "SUBJECTS": "#subjectsInput",
    "HOBBIES_SPORTS": "//label[text()='Sports']",
    "HOBBIES_READING": "//label[text()='Reading']",
    "HOBBIES_MUSIC": "//label[text()='Music']",
    "UPLOAD_PICTURE": "#uploadPicture",
    "CURRENT_ADDRESS": "#currentAddress",
    "STATE": "#react-select-3-input",
    "CITY": "#react-select-4-input",
    "SUBMIT_BUTTON": "#submit",
    "SUCCESS_MODAL": "#example-modal-sizes-title-lg",
    "CLOSE_MODAL": "#closeLargeModal",
}

class FormPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/automation-practice-form"

    def open(self):
        self.page.goto(self.url)

    def fill_basic_info(self, first, last, email, gender, mobile):
        self.page.locator(elements["FIRST_NAME"]).fill(first)
        self.page.locator(elements["LAST_NAME"]).fill(last)
        self.page.locator(elements["EMAIL"]).fill(email)
        self.page.locator(elements[f"GENDER_{gender.upper()}"]).click()
        self.page.locator(elements["MOBILE"]).fill(mobile)

    def fill_date_of_birth(self, dob):
        self.page.locator(elements["DATE_OF_BIRTH"]).fill(dob)

    def fill_subjects(self, subjects: list):
        for subject in subjects:
            self.page.locator(elements["SUBJECTS"]).fill(subject)
            self.page.keyboard.press("Enter")

    def select_hobbies(self, hobbies: list):
        for hobby in hobbies:
            self.page.locator(elements[f"HOBBIES_{hobby.upper()}"]).click()

    def fill_address(self, address):
        self.page.locator(elements["CURRENT_ADDRESS"]).fill(address)

    def select_state_city(self, state, city):
        self.page.locator(elements["STATE"]).fill(state)
        self.page.keyboard.press("Enter")
        self.page.locator(elements["CITY"]).fill(city)
        self.page.keyboard.press("Enter")

    def upload_file(self, file_path):
        self.page.locator(elements["UPLOAD_PICTURE"]).set_input_files(file_path)

    def submit_form(self):
        self.page.locator(elements["SUBMIT_BUTTON"]).click()

    def get_success_message(self):
        self.page.locator(elements["SUCCESS_MODAL"]).wait_for(state="visible")
        return self.page.locator(elements["SUCCESS_MODAL"]).inner_text()

    def close_modal(self):
        self.page.locator(elements["CLOSE_MODAL"]).click()

    def get_confirmation_data(self):
        self.page.locator("#example-modal-sizes-title-lg").wait_for(state="visible", timeout=5000)
        rows = self.page.locator("table tbody tr")
        data = {}
        for i in range(rows.count()):
            label = rows.nth(i).locator("td").nth(0).inner_text().strip()
            value = rows.nth(i).locator("td").nth(1).inner_text().strip()
            data[label] = value
        return data

    
    def is_field_red(self, field_name: str) -> bool:
        el = self.page.locator(elements[field_name])
        
        os.makedirs("screenshots", exist_ok=True)
        el.screenshot(path=f"screenshots/{field_name}_red_check.png")

        class_name = el.get_attribute("class") or ""
        border_color = el.evaluate("el => window.getComputedStyle(el).borderColor")
        return "error" in class_name.lower() or "rgb(220, 53, 69)" in border_color

    def is_field_green(self, field_name: str) -> bool:
        el = self.page.locator(elements[field_name])
        
        os.makedirs("screenshots", exist_ok=True)
        el.screenshot(path=f"screenshots/{field_name}_green_check.png")

        class_name = el.get_attribute("class") or ""
        border_color = el.evaluate("el => window.getComputedStyle(el).borderColor")
        return "success" in class_name.lower() or "rgb(40, 167, 69)" in border_color
