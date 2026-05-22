from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

from utilities.logger import get_logger

log = get_logger()


class BusSearchPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.log = get_logger()

    # =========================
    # LOCATORS
    # =========================

    FILTERS_TEXT = (
        By.XPATH,
        "//span[contains(text(),'Filters')]"
    )

    BUS_CARDS = (
        By.XPATH,
        "//div[contains(@class,'SrpActiveCardstyles')]"
    )

    AC_FILTER = (
        By.XPATH,
        "//span[contains(text(),'AC')]"
    )

    SLEEPER_FILTER = (
        By.XPATH,
        "//span[contains(text(),'Sleeper')]"
    )

    SORT_PRICE = (
        By.XPATH,
        "//span[contains(text(),'CHEAPEST')]"
    )

    SORT_DURATION = (
        By.XPATH,
        "//span[contains(text(),'DURATION')]"
    )

    VIEW_SEATS_BUTTONS = (
        By.XPATH,
        "(//span[contains(text(),'SELECT SEAT')])[2]"
    )

    # =========================
    # METHODS
    # =========================

    def verify_bus_results_displayed(self):

        log.info("Verifying bus results are displayed.")

        try:
            element = self.wait.until(
                EC.visibility_of_element_located(
                    self.FILTERS_TEXT
                )
            )

            return element.is_displayed()

        except Exception:
            return False

    def click_ac_filter(self):

        btn = self.wait.until(
            EC.element_to_be_clickable(
                self.AC_FILTER
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            btn
        )

        time.sleep(3)

    def click_sleeper_filter(self):

        btn = self.wait.until(
            EC.element_to_be_clickable(
                self.SLEEPER_FILTER
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            btn
        )

        time.sleep(3)

    def sort_by_price(self):

        log.info("Sorting by Price.")

        price = self.wait.until(
            EC.presence_of_element_located(
                self.SORT_PRICE
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            price
        )

        time.sleep(2)

        self.driver.execute_script(
            "arguments[0].click();",
            price
        )

        time.sleep(5)

    def sort_by_duration(self):

        log.info("Sorting by Duration.")

        duration = self.wait.until(
            EC.presence_of_element_located(
                self.SORT_DURATION
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            duration
        )

        time.sleep(2)

        self.driver.execute_script(
            "arguments[0].click();",
            duration
        )

        time.sleep(5)

    def get_bus_count(self):

        buses = self.driver.find_elements(
            *self.BUS_CARDS
        )

        return len(buses)

    def click_select_seat_second_bus(self):

        log.info("Clicking SELECT SEAT on second bus.")

        self.driver.execute_script(
            "window.scrollBy(0,700)"
        )

        time.sleep(3)

        btn = self.wait.until(
            EC.presence_of_element_located(
                self.VIEW_SEATS_BUTTONS
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            btn
        )

        time.sleep(5)