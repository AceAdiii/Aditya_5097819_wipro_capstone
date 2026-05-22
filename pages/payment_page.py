from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utilities.logger import get_logger

log = get_logger()


class PaymentPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.log = get_logger()


#     LOCATORS
    CARD_PAYMENT_OPTION = (
        By.XPATH,
        "//li[@data-testid='paymode-container'][.//p[@data-testid='paymode-title' and text()='Credit/Debit/ATM Card']]"
    )

    CARD_NUMBER_INPUT = (
        By.XPATH,
        "//input[@data-testid='card-fields-number-input']"
    )




#     METHODS

    def select_card_payment_option(self):
        log.info("Selecting Credit/Debit/ATM Card payment option.")

        card_option = self.wait.until(
            EC.element_to_be_clickable(self.CARD_PAYMENT_OPTION)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            card_option
        )

        card_option.click()

        log.info("Card payment option selected successfully.")

    def verify_cards_payment_page_loaded(self):

        log.info("Verifying Cards payment page loaded.")

        try:

            card_input = self.wait.until(
                EC.visibility_of_element_located(
                    self.CARD_NUMBER_INPUT
                )
            )

            log.info("Cards payment page loaded successfully.")

            return card_input.is_displayed()

        except Exception as e:

            log.error(
                f"Cards payment page verification failed: {e}"
            )

            return False