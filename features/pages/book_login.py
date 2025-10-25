from playwright.sync_api import Page
import os
from datetime import datetime

elements = {
    "USERNAME": "#userName",
    "PASSWORD": "#password",
    "LOGIN_BUTTON": "#login",
    "ERROR_MESSAGE": "#name",
    "LOGGED_IN_USER": ".mr-2",
    "LOGOUT_BUTTON": "button:has-text('Log out')", 
    "LOGGED_IN_USER": '//*[@id="userName-value"]',
    "REMEMBER_ME": "#rememberMe", 
}

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demoqa.com/login"
        self.elements = elements

    def open(self):
        self.page.goto(self.url)

    def fill_username(self, username: str):
        self.page.locator(self.elements["USERNAME"]).fill(username)

    def fill_password(self, password: str):
        self.page.locator(self.elements["PASSWORD"]).fill(password)

    def click_login(self):
        self.page.locator(self.elements["LOGIN_BUTTON"]).click()

    def login(self, username: str, password: str):
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        return self.page.locator(self.elements["ERROR_MESSAGE"]).inner_text()

    def get_logged_in_user(self) -> str:
        return self.page.locator(self.elements["LOGGED_IN_USER"]).inner_text()

    def is_login_successful(self) -> bool:
        return self.page.locator(self.elements["LOGGED_IN_USER"]).is_visible()

    def is_error_visible(self) -> bool:
        return self.page.locator(self.elements["ERROR_MESSAGE"]).is_visible()

    def screenshot_field(self, field_name: str, folder="screenshots") -> str:
        os.makedirs(folder, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.abspath(f"{folder}/{field_name}_{ts}.png")
        self.page.locator(self.elements[field_name]).screenshot(path=path)
        return path

    def screenshot_page(self, folder="screenshots") -> str:
        os.makedirs(folder, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.abspath(f"{folder}/page_{ts}.png")
        self.page.screenshot(path=path)
        return path
    
    def get_logged_in_user_element(self):
        return self.page.locator(self.elements["LOGGED_IN_USER"])
