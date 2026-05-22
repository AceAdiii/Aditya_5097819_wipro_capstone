import pytest
import os
import allure
from datetime import datetime
import undetected_chromedriver as uc

from utilities.logger import get_logger

logger = get_logger()

# =============================================================================
# REPORT FOLDERS
# =============================================================================

SCREENSHOT_DIR = "reports/screenshots"
ALLURE_RESULTS = "reports/allure-results"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(ALLURE_RESULTS, exist_ok=True)
os.makedirs("logs", exist_ok=True)

# =============================================================================
# DRIVER SETUP
# =============================================================================

@pytest.fixture(scope="function")
def setup():

    logger.info("========== STARTING TEST ==========")

    options = uc.ChromeOptions()

    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(options=options,version_main=148)

    driver.implicitly_wait(10)

    driver.get("https://www.goibibo.com/")

    logger.info("Goibibo launched successfully")

    yield driver

    logger.info("Closing browser")

    driver.quit()

    logger.info("========== TEST FINISHED ==========")

# =============================================================================
# ALLURE SCREENSHOTS + LOG ATTACHMENT
# =============================================================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call":

        driver = item.funcargs.get("setup")

        if driver:

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            status = "PASSED" if report.passed else "FAILED"

            screenshot_name = (
                f"{status}_{item.name}_{timestamp}.png"
            )

            screenshot_path = os.path.join(
                SCREENSHOT_DIR,
                screenshot_name
            )

            driver.save_screenshot(screenshot_path)

            logger.info(f"Screenshot saved: {screenshot_path}")

            # Attach screenshot to allure
            with open(screenshot_path, "rb") as image:

                allure.attach(
                    image.read(),
                    name=screenshot_name,
                    attachment_type=allure.attachment_type.PNG
                )

            # Attach logs
            log_path = "logs/execution.log"

            if os.path.exists(log_path):

                with open(log_path, "r") as file:

                    allure.attach(
                        file.read(),
                        name="Execution Logs",
                        attachment_type=allure.attachment_type.TEXT
                    )
