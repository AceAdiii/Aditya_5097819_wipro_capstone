from selenium.webdriver.common.by import By


class BusSearchLocators:
    FILTERS_TEXT = (By.XPATH, "//*[normalize-space()='Filters']")
    RESULT_SUMMARY = (
        By.XPATH,
        "//*[contains(normalize-space(),'Showing')]/following::*[contains(normalize-space(),'buses')][1]",
    )
    BUS_CARDS = (
        By.XPATH,
        "//div[contains(@class,'SrpActiveCardstyles__ActivecardLayoutDiv') "
        "and (.//button[contains(normalize-space(),'SELECT SEAT')] "
        "or .//button[contains(normalize-space(),'HIDE SEAT')])]",
    )
    AC_FILTER = (
        By.XPATH,
        "("
        "//div[contains(@class,'FiltersBlockstyles__BusTypeFilterTab')][normalize-space()='AC']"
        " | //span[normalize-space()='AC']"
        ")[1]",
    )
    SLEEPER_FILTER = (
        By.XPATH,
        "("
        "//div[contains(@class,'FiltersBlockstyles__BusTypeFilterTab')][normalize-space()='Sleeper']"
        " | //span[normalize-space()='Sleeper']"
        ")[1]",
    )
    SORT_PRICE = (By.XPATH, "(//*[normalize-space()='CHEAPEST'])[1]")
    SORT_DURATION = (
        By.XPATH,
        "(//*[normalize-space()='FASTEST' or normalize-space()='DURATION'])[1]",
    )
    SELECT_SEAT_BUTTONS = (By.XPATH, "//button[normalize-space()='SELECT SEAT']")
    HIDE_SEAT_BUTTON = (By.XPATH, "//button[normalize-space()='HIDE SEAT']")
    SHOW_BUSES_BUTTON = (By.XPATH, "//button[normalize-space()='SHOW BUSES']")
    NO_RESULTS_OR_ERROR = (
        By.XPATH,
        "//*[contains(translate(normalize-space(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'no bus') "
        "or contains(translate(normalize-space(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'oops') "
        "or contains(translate(normalize-space(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sorry')]",
    )

