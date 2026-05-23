from selenium.webdriver.common.by import By


class HomeLocators:
    BUS_TAB = (
        By.XPATH,
        "("
        "//a[contains(@href,'/bus')][.//*[normalize-space()='Bus'] or normalize-space()='Bus']"
        " | //span[normalize-space()='Bus']"
        ")[1]",
    )
    SOURCE_CITY_INPUT = (By.ID, "autosuggestBusSRPSrcHome")
    DESTINATION_CITY_INPUT = (By.ID, "autosuggestBusSRPDestHome")
    SEARCH_BUS_BUTTON = (
        By.XPATH,
        "//button[@data-testid='searchBusBtn' or normalize-space()='Search Bus']",
    )
    LOGIN_POPUP_CLOSE = (By.XPATH, "//span[@role='presentation']")
    GENERIC_POPUP_CLOSE = (
        By.XPATH,
        "("
        "//span[contains(@class,'logSprite')]"
        " | //span[contains(@class,'close')]"
        " | //button[contains(@aria-label,'close') or contains(@aria-label,'Close')]"
        ")[1]",
    )
    BUS_MODULE_HEADING = (
        By.XPATH,
        "//*[normalize-space()='Bus Ticket Booking' or normalize-space()='Search Bus']",
    )
    SAME_CITY_ERROR = (
        By.XPATH,
        "//*[contains(normalize-space(), \"Source and Destination can't be same\")]",
    )

