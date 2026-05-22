from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from utilities.logger import get_logger

log = get_logger()


class BusBookingPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 40)
        self.log = get_logger()

    # =========================
    # LOCATORS
    # =========================
    #
    # FIRST_BOARDING_POINT = (By.XPATH,
    #                         "(//div[contains(@class,'boxWrapper')]"
    #                         "[.//p[contains(@class,'boxHeaders') and normalize-space(text())='Boarding Point']]"
    #                         "//label[contains(@class,'LocationPointsstyles__listItem')])[1]"
    #                         )
    # FIRST_DROPPING_POINT = (By.XPATH,
    #                         "(//div[contains(@class,'boxWrapper')]"
    #                         "[.//p[contains(@class,'boxHeaders') and normalize-space(text())='Dropping Point']]"
    #                         "//label[contains(@class,'LocationPointsstyles__listItem')])[1]"
    #                         )

    # Locators - target the outer label (the full clickable card)
    FIRST_BOARDING_POINT = (
        By.XPATH,
        "(//div[contains(@class,'boxWrapper')]"
        "[.//p[contains(@class,'boxHeaders') and normalize-space(text())='Boarding Point']]"
        "//label[contains(@class,'LocationPointsstyles__listItem')])[1]"
    )

    FIRST_DROPPING_POINT = (
        By.XPATH,
        "(//div[contains(@class,'boxWrapper')]"
        "[.//p[contains(@class,'boxHeaders') and normalize-space(text())='Dropping Point']]"
        "//label[contains(@class,'LocationPointsstyles__listItem')])[1]"
    )

    # Confirmation locators - check for 'active' class to verify selection
    BOARDING_POINT_SELECTED = (
        By.XPATH,
        "(//div[contains(@class,'boxWrapper')]"
        "[.//p[contains(@class,'boxHeaders') and normalize-space(text())='Boarding Point']]"
        "//label[contains(@class,'LocationPointsstyles__listItem') and contains(@class,'active')])[1]"
    )

    DROPPING_POINT_SELECTED = (
        By.XPATH,
        "(//div[contains(@class,'boxWrapper')]"
        "[.//p[contains(@class,'boxHeaders') and normalize-space(text())='Dropping Point']]"
        "//label[contains(@class,'LocationPointsstyles__listItem') and contains(@class,'active')])[1]"
    )
    AVAILABLE_SEATS = (By.XPATH,
                       "(//div[contains(@class,'SeatWithTooltipstyles__BusSleeper')]"
                       "[.//*[contains(@class,'BusSleeperIcon')"
                       "      and not(contains(@class,'BusSleeperBookedIcon'))]])[1]"
                       )


    CONTINUE_BTN = (
        By.XPATH,
        "//button[contains(text(),'CONTINUE')]"
    )

    NO_INSURANCE = (
        By.XPATH,
        "//span[contains(text(),\"No, I don't need it\")]"
    )

    FULL_NAME = (
        By.XPATH,
        "//input[@placeholder='Enter Full Name']"
    )

    AGE = (
        By.XPATH,
        "//input[@placeholder='Age']"
    )

    EMAIL = (
        By.XPATH,
        "//input[@placeholder='Enter Email Address']"
    )

    MOBILE = (
        By.XPATH,
        "//input[@placeholder='Enter Mobile Number']"
    )

    BILLING_ADDRESS = (
        By.XPATH,
        "//input[@id='Billing Address']"
    )

    PINCODE = (
        By.XPATH,
        "//input[@id='Pincode']"
    )
    MALE_GENDER_OPTION = (
        By.XPATH,
        "//li[.//span[text()='Male']]"
    )

    CONFIRM_CHECKBOX = (By.XPATH, "//input[@type='checkbox' and @id='confirm_check']")

    PERSONAL_RADIO = (
        By.XPATH,
        "//label[@for='personalPersonal']"
    )

    PAY_BUTTON = (
        By.XPATH,
        "//button[contains(text(),'Pay')]"
    )

    # =========================
    # METHODS
    # =========================
    def select_boarding_point(self):
        log.info("Selecting first boarding point.")

        boarding = self.wait.until(
            EC.element_to_be_clickable(self.FIRST_BOARDING_POINT)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            boarding
        )
        time.sleep(0.5)

        # Click the inner radio input directly to avoid toggling
        radio = boarding.find_element(By.XPATH, ".//input[@type='radio']")
        self.driver.execute_script("arguments[0].click();", radio)

        # Verify 'active' class appears on the outer label
        self.wait.until(
            EC.presence_of_element_located(self.BOARDING_POINT_SELECTED)
        )

        log.info("Boarding point selected and confirmed.")
        time.sleep(0.5)  # let UI settle before dropping point

    def select_dropping_point(self):
        log.info("Selecting first dropping point.")

        dropping = self.wait.until(
            EC.element_to_be_clickable(self.FIRST_DROPPING_POINT)
        )

        # Check if already pre-selected (active class already present)
        already_selected = "active" in dropping.get_attribute("class")

        if already_selected:
            log.info("Dropping point already pre-selected, skipping click.")
        else:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                dropping
            )
            time.sleep(0.5)

            # Click the inner radio input directly
            radio = dropping.find_element(By.XPATH, ".//input[@type='radio']")
            self.driver.execute_script("arguments[0].click();", radio)

        # Verify 'active' class is present regardless
        self.wait.until(
            EC.presence_of_element_located(self.DROPPING_POINT_SELECTED)
        )

        log.info("Dropping point selected and confirmed.")
        time.sleep(0.5)  # let UI settle before seat selection

    def select_available_seat(self):

        log.info("Selecting first available seat.")

        seats = self.wait.until(
            EC.presence_of_all_elements_located(
                self.AVAILABLE_SEATS
            )
        )

        for seat in seats:

            try:

                if seat.is_displayed():
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});",
                        seat
                    )

                    self.driver.execute_script(
                        "arguments[0].click();",
                        seat
                    )

                    # Verify CONTINUE button appears
                    self.wait.until(
                        EC.visibility_of_element_located(
                            self.CONTINUE_BTN
                        )
                    )

                    log.info("Seat selected successfully.")
                    return

            except Exception:
                continue

        raise Exception("No available seat found.")

    def click_continue(self):

        log.info("Clicking CONTINUE button.")

        btn = self.wait.until(
            EC.element_to_be_clickable(self.CONTINUE_BTN)
        )

        btn.click()

    def click_no_insurance(self):

        try:

            btn = self.wait.until(
                EC.element_to_be_clickable(
                    self.NO_INSURANCE
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                btn
            )

            time.sleep(2)

        except Exception:
            log.info("Insurance popup not displayed.")

    def select_male_gender(self):

        log.info("Selecting Male gender option.")

        male_option = self.wait.until(
            EC.presence_of_element_located(
                self.MALE_GENDER_OPTION
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            male_option
        )

        self.driver.execute_script(
            "arguments[0].click();",
            male_option
        )

        log.info("Male gender selected successfully.")

    def fill_passenger_details(
            self,
            name,
            age,
            email,
            mobile,
            address,
            pincode
    ):

        self.wait.until(
            EC.visibility_of_element_located(
                self.FULL_NAME
            )
        ).send_keys(name)

        self.driver.find_element(
            *self.AGE
        ).send_keys(age)

        self.driver.find_element(
            *self.EMAIL
        ).send_keys(email)

        self.driver.find_element(
            *self.MOBILE
        ).send_keys(mobile)

        self.driver.find_element(
            *self.BILLING_ADDRESS
        ).send_keys(address)

        self.driver.find_element(
            *self.PINCODE
        ).send_keys(pincode)

        time.sleep(2)

    def click_confirm_checkbox(self):

        log.info("Looking for confirm checkbox...")

        for attempt in range(3):

            try:
                checkbox = self.wait.until(
                    EC.presence_of_element_located(self.CONFIRM_CHECKBOX)
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    checkbox
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    checkbox
                )

                log.info("Confirm checkbox clicked successfully.")

                return

            except Exception as e:
                log.warning(f"Retry {attempt + 1} failed: {e}")

        raise Exception("Unable to click confirm checkbox.")

    def select_personal(self):

        btn = self.wait.until(
            EC.element_to_be_clickable(
                self.PERSONAL_RADIO
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            btn
        )

    def click_pay_button(self):

        btn = self.wait.until(
            EC.element_to_be_clickable(
                self.PAY_BUTTON
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            btn
        )

        time.sleep(5)