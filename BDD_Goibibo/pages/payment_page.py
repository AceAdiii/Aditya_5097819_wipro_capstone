from locators.payment_locators import PaymentLocators
from pages.base_page import BasePage


class PaymentPage(BasePage):
    def select_card_payment_option(self):
        self.log.info("Selecting Credit/Debit/ATM Card payment option.")
        self.find_visible(PaymentLocators.PAYMENT_OPTIONS_TITLE, timeout=35)
        self.click(PaymentLocators.CARD_PAYMENT_OPTION, timeout=20)
        self.find_visible(PaymentLocators.CARD_NUMBER_INPUT, timeout=25)

    def is_card_payment_page_loaded(self):
        self.log.info("Verifying card payment page.")
        return self.is_visible(PaymentLocators.CARD_NUMBER_INPUT, timeout=20)

