from selenium.webdriver.common.by import By


class BusBookingLocators:
    BOARDING_POINT_TEXT = (By.XPATH, "//p[normalize-space()='Boarding Point']")
    DROPPING_POINT_TEXT = (By.XPATH, "//p[normalize-space()='Dropping Point']")
    FIRST_BOARDING_POINT = (
        By.XPATH,
        "(//p[normalize-space()='Boarding Point']"
        "/following::label[contains(@class,'LocationPointsstyles__listItem')])[1]",
    )
    FIRST_DROPPING_POINT = (
        By.XPATH,
        "(//p[normalize-space()='Dropping Point']"
        "/following::label[contains(@class,'LocationPointsstyles__listItem')])[1]",
    )
    AVAILABLE_SEATS = (
        By.XPATH,
        "//div[contains(@class,'SeatWithTooltipstyles__BusSleeper') "
        "or contains(@class,'SeatWithTooltipstyles__BusSeat')]"
        "[.//*[contains(@class,'Icon') "
        "and not(contains(@class,'Booked')) "
        "and not(contains(@class,'Ladies')) "
        "and not(contains(@class,'Selected'))]]",
    )
    CONTINUE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='CONTINUE' or contains(normalize-space(),'PROCEED')]",
    )
    REVIEW_BOOKING_MARKER = (
        By.XPATH,
        "//*[contains(normalize-space(),'Review your Booking') "
        "or @id='goAssurance' "
        "or @id='travellerForm1']",
    )
    POINT_SELECTION_ERROR = (
        By.XPATH,
        "//*[contains(normalize-space(),'Please select boarding and dropping point to proceed')]",
    )
    NO_INSURANCE_OPTION = (
        By.XPATH,
        "("
        "//label[.//span[normalize-space()=\"No, I don't need it\"]]"
        " | //span[normalize-space()=\"No, I don't need it\"]"
        " | //*[@id=\"cancelNo, I don't need it\"]"
        " | //label[.//*[normalize-space()=\"No, I'll risk it\"]]"
        " | //*[normalize-space()=\"No, I'll risk it\"]"
        ")[1]",
    )
    FULL_NAME_INPUT = (By.XPATH, "//input[@placeholder='Enter Full Name']")
    AGE_INPUT = (By.XPATH, "//input[@placeholder='Age']")
    EMAIL_INPUT = (By.XPATH, "//input[@placeholder='Enter Email Address']")
    MOBILE_INPUT = (By.XPATH, "//input[@placeholder='Enter Mobile Number']")
    MALE_GENDER_OPTION = (
        By.XPATH,
        "(//li[.//span[normalize-space()='Male']] | //span[normalize-space()='Male']/ancestor::li[1])[1]",
    )
    BILLING_ADDRESS_INPUT = (By.ID, "Billing Address")
    PINCODE_INPUT = (By.ID, "Pincode")
    CONFIRM_BILLING_CHECKBOX = (By.ID, "confirm_check")
    PERSONAL_TRIP_OPTION = (
        By.XPATH,
        "("
        "//label[@for='personalPersonal']"
        " | //span[normalize-space()='Personal']/ancestor::label[1]"
        " | //*[normalize-space()='Personal']/ancestor::*[self::label or self::div][1]"
        ")[1]",
    )
    PAY_BUTTON = (By.XPATH, "//button[contains(normalize-space(),'Pay')]")
