#!/bin/bash

RESULTS_DIR=/app/reports/allure-results
REPORT_DIR=/app/reports/allure-report

rm -rf $RESULTS_DIR/*
rm -rf $REPORT_DIR/*


behave features/web_table.feature -f allure_behave.formatter:AllureFormatter -o $RESULTS_DIR || true
behave features/book_login.feature -f allure_behave.formatter:AllureFormatter -o $RESULTS_DIR || true
behave features/form.feature -f allure_behave.formatter:AllureFormatter -o $RESULTS_DIR || true


allure generate $RESULTS_DIR -o $REPORT_DIR --clean

echo "✅ Allure report generated at $REPORT_DIR/index.html"
