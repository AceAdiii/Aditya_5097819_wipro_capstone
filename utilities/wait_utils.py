from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utilities.logger import get_logger

log = get_logger("wait_utils")


class WaitUtils:

    def __init__(self, driver, timeout=20):

        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # =========================================================================
    # CLICK ELEMENT
    # =========================================================================

    def click(self, locator):

        try:

            element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )

            element.click()

            log.info(f"Clicked element: {locator}")

        except TimeoutException:

            log.error(f"Unable to click element: {locator}")

            raise

    # =========================================================================
    # SEND KEYS
    # =========================================================================

    def send_keys(self, locator, value):

        try:

            element = self.wait.until(
                EC.visibility_of_element_located(locator)
            )

            element.clear()

            element.send_keys(value)

            log.info(f"Entered text into: {locator}")

        except TimeoutException:

            log.error(f"Unable to enter text into: {locator}")

            raise

    # =========================================================================
    # WAIT FOR VISIBILITY
    # =========================================================================

    def visible(self, locator):

        try:

            element = self.wait.until(
                EC.visibility_of_element_located(locator)
            )

            log.info(f"Element visible: {locator}")

            return element

        except TimeoutException:

            log.error(f"Element not visible: {locator}")

            raise

    # =========================================================================
    # WAIT FOR PRESENCE
    # =========================================================================

    def present(self, locator):

        try:

            element = self.wait.until(
                EC.presence_of_element_located(locator)
            )

            log.info(f"Element present: {locator}")

            return element

        except TimeoutException:

            log.error(f"Element not present: {locator}")

            raise

    # =========================================================================
    # WAIT FOR INVISIBILITY
    # =========================================================================

    def invisible(self, locator):

        try:

            result = self.wait.until(
                EC.invisibility_of_element_located(locator)
            )

            log.info(f"Element invisible: {locator}")

            return result

        except TimeoutException:

            log.error(f"Element still visible: {locator}")

            raise

    # =========================================================================
    # GET TEXT
    # =========================================================================

    def get_text(self, locator):

        try:

            element = self.wait.until(
                EC.visibility_of_element_located(locator)
            )

            text = element.text

            log.info(f"Fetched text from: {locator}")

            return text

        except TimeoutException:

            log.error(f"Unable to get text from: {locator}")

            raise