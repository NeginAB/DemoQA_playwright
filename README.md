# DemoQA Playwright Automation

Automated testing framework for the **DemoQA** web application using **Playwright**, **Behave (BDD)**, and **Python**. Fully **Dockerized** with **Allure reporting** for test results.

---

## Key Features

- BDD-style test scenarios using Behave
- End-to-end tests for:
  - Web tables
  - Forms
  - Login functionality
- Test automation using **Playwright (Chromium)**
- Dockerized environment for consistent cross-platform execution
- Automated **Allure HTML reports** with screenshots on failure
- Headless browser execution inside Docker
- Ready for CI/CD integration (GitHub Actions or other pipelines)

---

## Project Structure



demoqa-playwright/
├── features/ # BDD feature files
│ ├── web_table.feature
│ ├── book_login.feature
│ └── form.feature
├── reports/ # Allure results and reports
├── run_tests.sh # Script to run all tests and generate reports
├── Dockerfile # Docker setup
├── requirements.txt # Python dependencies
├── features/environment.py # Playwright & Behave hooks
└── .github/workflows/ # CI/CD workflows


---

## Getting Started

### 1. Build Docker Image

```bash
docker build -t demoqa-tests .

2. Run All Tests Inside Docker

This runs all features (web_table, book_login, form) headlessly and generates Allure results:

docker run --rm -v $(pwd)/reports:/app/reports demoqa-tests


-v $(pwd)/reports:/app/reports mounts the local reports folder to save results.

3. Run Individual Feature (Optional)
docker run --rm -v $(pwd)/reports:/app/reports demoqa-tests behave features/web_table.feature -f allure_behave.formatter:AllureFormatter -o /app/reports/allure-results

4. Access Allure Report

Allure report is generated automatically after tests. To manually generate or open:

allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report


Reports include screenshots of failed steps.

CI/CD Integration

GitHub Actions workflow runs all features automatically

Supports manual triggers and scheduled runs

Allure reports can be uploaded as artifacts

Docker ensures headless execution in CI environments

Notes

Screenshots for failed steps are stored in reports/screenshots

Docker image requires at least 2GB free for Chromium installation

Allure version: 2.27.0

Python version: 3.12