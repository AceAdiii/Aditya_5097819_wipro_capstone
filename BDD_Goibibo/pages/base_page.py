import time

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config_reader import config
from utils.logger import get_logger


def xpath_literal(value):
    value = str(value)
    if '"' not in value:
        return f'"{value}"'
    if "'" not in value:
        return f"'{value}'"
    return "concat(" + ", '\"', ".join(f'"{part}"' for part in value.split('"')) + ")"


class BasePage:
    def __init__(self, driver, timeout=None):
        self.driver = driver
        self.timeout = timeout or config.get_int("basic info", "explicit_wait", 35)
        self.wait = WebDriverWait(driver, self.timeout)
        self.log = get_logger()

    def wait_for_page_ready(self, timeout=30):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") in {"interactive", "complete"}
        )

    def find_visible(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def find_present(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_clickable(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_any_visible(self, locators, timeout=None):
        last_error = None
        end_time = time.time() + (timeout or self.timeout)

        while time.time() < end_time:
            for locator in locators:
                try:
                    return WebDriverWait(self.driver, 1).until(
                        EC.visibility_of_element_located(locator)
                    )
                except TimeoutException as error:
                    last_error = error
            time.sleep(0.2)

        raise last_error or TimeoutException("No locator became visible.")

    def is_visible(self, locator, timeout=3):
        try:
            return self.find_visible(locator, timeout=timeout).is_displayed()
        except Exception:
            return False

    def visible_elements(self, locator, timeout=None):
        self.find_present(locator, timeout=timeout)
        return [element for element in self.driver.find_elements(*locator) if element.is_displayed()]

    def scroll_to(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'nearest'});", element)
        time.sleep(0.2)

    def click(self, locator, timeout=None, use_js=True):
        last_error = None

        for attempt in range(3):
            try:
                element = self.find_clickable(locator, timeout=timeout)
                self.scroll_to(element)
                if use_js:
                    self.driver.execute_script("arguments[0].click();", element)
                else:
                    element.click()
                return element
            except (ElementClickInterceptedException, StaleElementReferenceException, TimeoutException) as error:
                last_error = error
                self.log.warning(f"Click retry {attempt + 1} failed for {locator}: {error}")
                time.sleep(1)

        raise last_error

    def safe_click(self, locator, timeout=5, use_js=True):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
            self.scroll_to(element)
            if use_js:
                self.driver.execute_script("arguments[0].click();", element)
            else:
                element.click()
            return True
        except Exception as error:
            self.log.info(f"Optional click skipped for {locator}: {error.__class__.__name__}")
            return False

    def type_text(self, locator, value, timeout=None, clear=True):
        element = self.find_visible(locator, timeout=timeout)
        self.scroll_to(element)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].focus(); arguments[0].click();", element)
        if clear:
            element.send_keys(Keys.CONTROL, "a")
            element.send_keys(Keys.BACKSPACE)
        element.send_keys(str(value))
        return element

    def get_text(self, locator, timeout=None):
        return self.find_visible(locator, timeout=timeout).text

    def wait_url_contains(self, text, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(EC.url_contains(text))
