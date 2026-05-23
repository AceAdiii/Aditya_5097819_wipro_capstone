from selenium.webdriver.common.by import By


class PaymentLocators:
    PAYMENT_OPTIONS_TITLE = (
        By.XPATH,
        "//*[normalize-space()='Payment Options' or normalize-space()='ALL PAYMENT OPTIONS']",
    )
    CARD_PAYMENT_OPTION = (
        By.XPATH,
        "("
        "//*[normalize-space()='Credit/Debit/ATM Card']/ancestor::*[self::li or self::div][1]"
        " | //p[normalize-space()='Credit/Debit/ATM Card']"
        ")[1]",
    )
    CARD_PAGE_TITLE = (
        By.XPATH,
        "//*[@data-testid='cards-landing-page-title' or normalize-space()='Cards']",
    )
    CARD_NUMBER_INPUT = (
        By.XPATH,
        "//*[@data-testid='card-fields-number-input' "
        "or @id='cardNumber' "
        "or @placeholder='ENTER CARD NUMBER']",
    )

