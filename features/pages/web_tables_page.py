from playwright.sync_api import Page
import os
from datetime import datetime

elements = {
    "ADD_BUTTON": "#addNewRecordButton",
    "MODAL_SUBMIT": "#submit",
    "EDIT_BUTTON": "span[title='Edit']",
    "DELETE_BUTTON": "span[title='Delete']",
    "TABLE_ROWS": ".rt-tbody .rt-tr-group",
    "SEARCH_BOX": "#searchBox",
    "COLUMN_FIRST_NAME": "div.rt-resizable-header-content:text('First Name')",
    "COLUMN_LAST_NAME": "div.rt-resizable-header-content:text('Last Name')",
    "COLUMN_AGE": "div.rt-resizable-header-content:text('Age')",
    "COLUMN_EMAIL": "div.rt-resizable-header-content:text('Email')",
    "COLUMN_SALARY": "div.rt-resizable-header-content:text('Salary')",
    "COLUMN_DEPARTMENT": "div.rt-resizable-header-content:text('Department')",
    "COLUMN_ACTION": "div.rt-resizable-header-content:text('Action')",
    "MODAL_FIRST_NAME": "#firstName",
    "MODAL_LAST_NAME": "#lastName",
    "MODAL_EMAIL": "#userEmail",
    "MODAL_AGE": "#age",
    "MODAL_SALARY": "#salary",
    "MODAL_DEPARTMENT": "#department",
}


class WebTablesPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/webtables"
        self.elements = elements

    def open(self):
        self.page.goto(self.url)

    def screenshot_page(self, folder="screenshots"):
        os.makedirs(folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.abspath(f"{folder}/webtable_{timestamp}.png")
        self.page.screenshot(path=path)
        return path

    def click_add(self):
        self.page.locator(self.elements["ADD_BUTTON"]).click()

    def fill_form(self, first_name, last_name, email, age, salary, department):
        self.page.locator(self.elements["MODAL_FIRST_NAME"]).fill(first_name)
        self.page.locator(self.elements["MODAL_LAST_NAME"]).fill(last_name)
        self.page.locator(self.elements["MODAL_EMAIL"]).fill(email)
        self.page.locator(self.elements["MODAL_AGE"]).fill(str(age))
        self.page.locator(self.elements["MODAL_SALARY"]).fill(str(salary))
        self.page.locator(self.elements["MODAL_DEPARTMENT"]).fill(department)

    def submit_form(self):
        self.page.locator(self.elements["MODAL_SUBMIT"]).click()

    def get_all_rows(self):
        rows = self.page.locator(self.elements["TABLE_ROWS"])
        data = []
        for i in range(rows.count()):
            cells = rows.nth(i).locator(".rt-td")
            row_data = [cells.nth(j).inner_text().strip() for j in range(cells.count())]
            data.append(row_data)
        return data

    def get_row_by_email(self, email: str):
        for row in self.get_all_rows():
            if email in row:
                return row
        return None

    def search(self, text: str):
        self.page.locator(self.elements["SEARCH_BOX"]).fill(text)
        self.page.wait_for_timeout(300)

    def click_edit_row(self, index=0):
        self.page.locator(self.elements["EDIT_BUTTON"]).nth(index).click()


    def click_delete_row(self, index=0):
        self.page.locator(self.elements["DELETE_BUTTON"]).nth(index).click()

    def assert_row_exists(self, email: str):
        row = self.get_row_by_email(email)
        assert row is not None, f"Row with email '{email}' not found"

    def assert_row_not_exists(self, email: str):
        row = self.get_row_by_email(email)
        assert row is None, f"Row with email '{email}' should have been deleted"

    def assert_row_data(self, email: str, expected_data: dict):
        row = self.get_row_by_email(email)
        assert row is not None, f"Row with email '{email}' not found"
        keys = ["first_name", "last_name", "age", "email", "salary", "department"]
        for i, key in enumerate(keys):
            expected_value = str(expected_data[key])
            actual_value = row[i]
            assert actual_value == expected_value, f"{key} mismatch: expected {expected_value}, got {actual_value}"

    def assert_row_not_in_table(self, expected_data: dict):
        rows = self.get_all_rows()
        keys = ["first_name", "last_name", "age", "email", "salary", "department"]
        for row in rows:
            match = True
            for i, key in enumerate(keys):
                if str(expected_data[key]) != row[i]:
                    match = False
                    break
            if match:
                raise AssertionError(f"Deleted row still found in the table: {row}")


    
