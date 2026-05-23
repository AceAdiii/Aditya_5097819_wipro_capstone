# BDD_Goibibo

Behave BDD automation project for the Goibibo bus module using Selenium, POM, logs, screenshots, tags, and Allure reporting.

## Run

```powershell
pip install -r requirements.txt
python runtest.py --tags "@smoke"
```

Useful tags:

- `@smoke` runs the valid search and E2E payment-page flow.
- `@positive` runs the five positive bus-search scenarios.
- `@negative` runs the two validation scenarios.
- `@e2e` runs the home-to-card-payment-page journey.
- `@regression` runs the full suite.

Allure raw results are written to `reports/allure-results`. If the Allure CLI is installed, `runtest.py` also generates `reports/allure-report`.

The E2E test stops at the card payment form and does not enter card details or make a payment.

