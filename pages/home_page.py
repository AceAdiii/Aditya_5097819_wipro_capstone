from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time

from utilities.logger import get_logger

log = get_logger()


class HomePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        self.log = get_logger()

    # =========================
    # LOCATORS
    # =========================

    BUS_TAB = (
        By.XPATH,
        "//span[text()='Bus']"
    )
    SAME_CITY_ERROR = (By.XPATH, "//label[contains(text(),\"Source and Destination can't be same\")]")

    SOURCE_CITY_INPUT = (
        By.XPATH,
        "//input[@id='autosuggestBusSRPSrcHome']"
    )

    DESTINATION_INPUT = (
        By.XPATH,
        "//input[@id='autosuggestBusSRPDestHome']"
    )

    SEARCH_BUTTON = (
        By.XPATH,
        "//button[@data-testid='searchBusBtn']"
    )

    LOGIN_POPUP_CLOSE = (
        By.XPATH,
        "//span[@role='presentation']"
    )

    GENERIC_POPUP_CLOSE = (
        By.XPATH,
        "//span[contains(@class,'logSprite')]"
    )

    # =========================
    # METHODS
    # =========================

    def close_popup(self):
        try:
            popup = WebDriverWait(self.driver, 8).until(
                EC.element_to_be_clickable(self.GENERIC_POPUP_CLOSE)
            )
            popup.click()
            log.info("Generic popup closed.")

        except Exception:
            log.info("Generic popup not present – skipping.")

    def close_login_popup(self):
        try:
            login = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.LOGIN_POPUP_CLOSE)
            )
            login.click()
            log.info("Login popup closed.")

        except Exception:
            log.info("Login popup not present – skipping.")

    def click_bus_button(self):
        log.info("Clicking Bus tab.")

        bus = self.wait.until(
            EC.element_to_be_clickable(self.BUS_TAB)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            bus
        )

    def enter_source_city(self, city):

        log.info(f"Entering source city: {city}")

        for attempt in range(3):

            try:

                source_input = self.wait.until(
                    EC.presence_of_element_located(
                        self.SOURCE_CITY_INPUT
                    )
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    source_input
                )

                source_input.clear()

                source_input.send_keys(city)

                suggestion = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            f"(//span[contains(text(),'{city}')])[1]"
                        )
                    )
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    suggestion
                )

                log.info(f"Selected source city: {city}")

                return

            except StaleElementReferenceException:

                log.warning(
                    f"Stale element occurred while entering source city. Retry {attempt + 1}"
                )

        raise Exception("Unable to enter source city.")

    def enter_destination_city(self, city):

        log.info(f"Entering destination city: {city}")

        for attempt in range(3):

            try:

                dest_input = self.wait.until(
                    EC.presence_of_element_located(
                        self.DESTINATION_INPUT
                    )
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    dest_input
                )

                dest_input.clear()

                dest_input.send_keys(city)

                suggestion = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            f"(//span[contains(text(),'{city}')])[1]"
                        )
                    )
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    suggestion
                )

                log.info(f"Selected destination city: {city}")

                return

            except StaleElementReferenceException:

                log.warning(
                    f"Stale element occurred while entering destination city. Retry {attempt + 1}"
                )

        raise Exception("Unable to enter destination city.")



    def click_search_button(self):

        log.info("Clicking Search Bus button.")

        btn = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_BUTTON)
        )

        self.driver.execute_script(
            "arguments[0].click();",
            btn
        )

    def get_same_city_error_message(self):
        #
        error = self.wait.until(
            EC.visibility_of_element_located(self.SAME_CITY_ERROR)
        )

        return error.text
