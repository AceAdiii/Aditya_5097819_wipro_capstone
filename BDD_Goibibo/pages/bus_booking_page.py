import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains

from locators.bus_booking_locators import BusBookingLocators
from pages.base_page import BasePage


class BusBookingPage(BasePage):
    def select_boarding_point(self):
        self.log.info("Selecting first boarding point.")
        self.find_visible(BusBookingLocators.BOARDING_POINT_TEXT, timeout=25)
        self._select_location_point(BusBookingLocators.FIRST_BOARDING_POINT)

    def select_dropping_point(self):
        self.log.info("Selecting first dropping point.")
        self.find_visible(BusBookingLocators.DROPPING_POINT_TEXT, timeout=25)
        self._select_location_point(BusBookingLocators.FIRST_DROPPING_POINT)

    def _select_location_point(self, locator):
        label = self.find_visible(locator, timeout=20)
        self.scroll_to(label)
        try:
            ActionChains(self.driver).move_to_element(label).pause(0.1).click(label).perform()
        except Exception:
            try:
                radio = label.find_element("xpath", ".//input[@type='radio']")
                radio.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", label)
        time.sleep(0.5)

        selected = self.driver.execute_script(
            """
            const label = arguments[0];
            const input = label.querySelector('input[type="radio"], input[type="checkbox"]');
            if (input && input.checked) {
                return true;
            }

            const selectedClass = /selected|active|checked/i;
            if (selectedClass.test(label.className || '')) {
                return true;
            }

            return Array.from(label.querySelectorAll('*')).some((el) =>
                selectedClass.test(el.className || '') ||
                el.getAttribute('aria-checked') === 'true'
            );
            """,
            label,
        )
        if not selected:
            self.driver.execute_script(
                """
                const label = arguments[0];
                const clickable = label.querySelector('span, div, input') || label;
                clickable.click();
                """,
                label,
            )
            time.sleep(0.5)

    def select_available_seat(self):
        self.log.info("Selecting first available seat.")
        seats = self.visible_elements(BusBookingLocators.AVAILABLE_SEATS, timeout=25)

        for seat in seats:
            try:
                self.scroll_to(seat)
                self.driver.execute_script("arguments[0].click();", seat)
                self.find_visible(BusBookingLocators.CONTINUE_BUTTON, timeout=8)
                self.log.info("Seat selected successfully.")
                return
            except Exception as error:
                self.log.warning(f"Seat click failed, trying next available seat: {error}")

        raise AssertionError("No selectable bus seat was found.")

    def select_first_boarding_dropping_and_seat(self):
        self.select_boarding_point()
        self.select_available_seat()
        self.select_dropping_point()

    def click_continue(self):
        self.log.info("Continuing to traveller details.")
        for attempt in range(2):
            self.click(BusBookingLocators.CONTINUE_BUTTON, timeout=20)
            try:
                self.find_visible(BusBookingLocators.REVIEW_BOOKING_MARKER, timeout=20)
                return
            except TimeoutException:
                if not self.is_visible(BusBookingLocators.POINT_SELECTION_ERROR, timeout=2):
                    raise
                self.log.warning("Boarding/dropping selection was not accepted. Selecting points again.")
                self.select_boarding_point()
                self.select_dropping_point()

        self.click(BusBookingLocators.CONTINUE_BUTTON, timeout=20)
        self.find_visible(BusBookingLocators.REVIEW_BOOKING_MARKER, timeout=35)

    def skip_insurance(self):
        self.log.info("Skipping travel insurance if the option is shown.")
        self.safe_click(BusBookingLocators.NO_INSURANCE_OPTION, timeout=12)
        time.sleep(0.5)

    def fill_passenger_details(self, name, age, email, mobile, address, pincode):
        self.log.info("Filling passenger and billing details.")
        self.type_text(BusBookingLocators.FULL_NAME_INPUT, name, timeout=20)
        self.type_text(BusBookingLocators.AGE_INPUT, age)
        self.select_male_gender()
        self.type_text(BusBookingLocators.EMAIL_INPUT, email)
        self.type_text(BusBookingLocators.MOBILE_INPUT, mobile)
        self.type_text(BusBookingLocators.BILLING_ADDRESS_INPUT, address, timeout=20)
        self.type_text(BusBookingLocators.PINCODE_INPUT, pincode, timeout=20)
        time.sleep(1.5)

    def select_male_gender(self):
        self.log.info("Selecting Male gender.")
        self.click(BusBookingLocators.MALE_GENDER_OPTION, timeout=12)

    def confirm_billing_details(self):
        self.log.info("Confirming billing details if checkbox is available.")
        try:
            checkbox = self.find_present(BusBookingLocators.CONFIRM_BILLING_CHECKBOX, timeout=8)
            self.scroll_to(checkbox)
            if not checkbox.is_selected():
                self.driver.execute_script("arguments[0].click();", checkbox)
        except TimeoutException:
            self.log.info("Confirm billing checkbox was not displayed.")

    def select_personal_trip(self):
        self.log.info("Selecting Personal trip type if available.")
        self.safe_click(BusBookingLocators.PERSONAL_TRIP_OPTION, timeout=6)

    def confirm_billing_and_personal_trip(self):
        self.confirm_billing_details()
        self.select_personal_trip()

    def click_pay_button(self):
        self.log.info("Proceeding to payment.")
        self.click(BusBookingLocators.PAY_BUTTON, timeout=25)
        self.wait_url_contains("payments.goibibo.com", timeout=45)
