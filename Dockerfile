FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl unzip openjdk-21-jre-headless wget gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN curl -o /tmp/allure-2.27.0.zip -L https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.zip \
    && unzip /tmp/allure-2.27.0.zip -d /opt/ \
    && ln -s /opt/allure-2.27.0/bin/allure /usr/bin/allure

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps chromium
RUN mkdir -p /app/reports/allure-results /app/reports/allure-report

COPY run_tests.sh /app/run_tests.sh
RUN chmod +x /app/run_tests.sh
CMD ["/app/run_tests.sh"]
