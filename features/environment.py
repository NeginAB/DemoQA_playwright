import os
from datetime import datetime
from playwright.sync_api import sync_playwright
import allure

REPORTS_DIR = "/app/reports"
SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def before_all(context):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=True)
    context.context = context.browser.new_context()
    context.page = context.context.new_page()
    context.base_url = "https://demoqa.com"

def before_scenario(context, scenario):
    context.scenario_name = scenario.name

def after_step(context, step):
    if step.status == "failed":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = context.scenario_name.replace(" ", "_")
        screenshot_path = os.path.join(SCREENSHOTS_DIR, f"{safe_name}_{timestamp}.png")
        context.page.screenshot(path=screenshot_path)
        with open(screenshot_path, "rb") as f:
            allure.attach(f.read(), name=f"{step.name}", attachment_type=allure.attachment_type.PNG)

def after_all(context):
    if hasattr(context, "page"):
        context.page.close()
    if hasattr(context, "context"):
        context.context.close()
    if hasattr(context, "browser"):
        context.browser.close()
    if hasattr(context, "playwright"):
        context.playwright.stop()

