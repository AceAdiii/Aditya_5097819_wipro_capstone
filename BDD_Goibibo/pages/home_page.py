import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from locators.home_locators import HomeLocators
from pages.base_page import BasePage, xpath_literal
from utils.config_reader import config


class HomePage(BasePage):
    def open_home_page(self):
        url = config.get("basic info", "url", "https://www.goibibo.com/")
        self.log.info(f"Opening Goibibo home page: {url}")
        self.driver.get(url)
        self.wait_for_page_ready()
        self.close_popups()

    def open_bus_module(self):
        self.open_home_page()

        self.log.info("Opening Bus module from home page navigation.")
        clicked_bus_tab = self.safe_click(HomeLocators.BUS_TAB, timeout=6)

        try:
            if not clicked_bus_tab:
                raise TimeoutException("Bus tab was not clickable.")
            self.wait_for_page_ready()
            self.find_visible(HomeLocators.SOURCE_CITY_INPUT, timeout=20)
        except Exception as error:
            bus_url = config.get("basic info", "bus_url", "https://www.goibibo.com/bus/")
            self.log.warning(f"Bus tab navigation failed, opening Bus URL directly. Error: {error}")
            self.driver.get(bus_url)
            self.wait_for_page_ready()
            self.close_popups()
            self.find_visible(HomeLocators.SOURCE_CITY_INPUT, timeout=25)

    def close_popups(self):
        self.safe_click(HomeLocators.GENERIC_POPUP_CLOSE, timeout=4)
        self.safe_click(HomeLocators.LOGIN_POPUP_CLOSE, timeout=3)
        try:
            self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
        except Exception:
            pass

    def enter_source_city(self, city):
        self._enter_city(HomeLocators.SOURCE_CITY_INPUT, city, "source")

    def enter_destination_city(self, city):
        self._enter_city(HomeLocators.DESTINATION_CITY_INPUT, city, "destination")

    def _enter_city(self, input_locator, city, field_name):
        if not city:
            self.log.info(f"Leaving {field_name} city blank.")
            return

        self.log.info(f"Entering {field_name} city: {city}")

        for attempt in range(3):
            try:
                element = self.find_visible(input_locator, timeout=20)
                self.scroll_to(element)
                self.driver.execute_script("arguments[0].click();", element)
                element.send_keys(Keys.CONTROL, "a")
                element.send_keys(Keys.BACKSPACE)
                element.send_keys(city)

                exact_option = (
                    By.XPATH,
                    "(//div[@role='option']"
                    f"[normalize-space()={xpath_literal(city)} "
                    f"or .//span[normalize-space()={xpath_literal(city)}]])[1]",
                )
                contains_option = (
                    By.XPATH,
                    "(//div[@role='option']"
                    f"[contains(normalize-space(), {xpath_literal(city)}) "
                    f"or .//span[contains(normalize-space(), {xpath_literal(city)})]])[1]",
                )

                option_to_click = exact_option if self.is_visible(exact_option, timeout=2) else contains_option
                self.click(option_to_click, timeout=12)

                time.sleep(0.5)
                return
            except Exception as error:
                self.log.warning(f"Retry {attempt + 1}: unable to select {field_name} city {city}: {error}")
                time.sleep(1)

        raise AssertionError(f"Unable to enter {field_name} city: {city}")

    def click_search_button(self):
        self.log.info("Clicking Search Bus button.")
        self.click(HomeLocators.SEARCH_BUS_BUTTON, timeout=20)
        time.sleep(1)

    def search_buses(self, source, destination):
        self.enter_source_city(source)
        self.enter_destination_city(destination)
        self.click_search_button()

    def same_city_error_message(self):
        return self.get_text(HomeLocators.SAME_CITY_ERROR, timeout=10)
