import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.allure_helper import attach_screenshot
from pages.home_page import HomePage
from pages.bus_search_page import BusSearchPage
from pages.bus_booking_page import BusBookingPage
from pages.payment_page import PaymentPage

from utilities.logger import get_logger

log = get_logger()


@allure.feature("Bus Booking")
@allure.story("End To End Booking")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description(
    "Verify user can complete bus booking till payment page"
)
@allure.tag("Smoke", "Regression", "E2E")

class TestBusE2E:

    @allure.title(
        "E2E | Home → Search → Seat → Passenger → Payment"
    )

    def test_bus_e2e_home_to_payment(self, setup):

        driver = setup

        home_page = HomePage(driver)
        search_page = BusSearchPage(driver)
        booking_page = BusBookingPage(driver)
        payment_page = PaymentPage(driver)


        # HOME PAGE


        with allure.step("Close homepage popup"):
            home_page.close_popup()

        with allure.step("Close login popup"):
            home_page.close_login_popup()

        with allure.step("Click Bus section"):
            home_page.click_bus_button()
            attach_screenshot(driver,"Bus tab clicked")

        with allure.step("Enter source city"):
            home_page.enter_source_city("Delhi")

        with allure.step("Enter destination city"):
            home_page.enter_destination_city("Mussoorie")

        with allure.step("Click search button"):
            home_page.click_search_button()
            attach_screenshot(driver, "Search results loaded")


        # RESULTS PAGE


        with allure.step("Verify bus search results displayed"):
            assert search_page.verify_bus_results_displayed()

        with allure.step("Select seat from second bus"):
            search_page.click_select_seat_second_bus()

        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//p[contains(text(),'Boarding Point')]"
            ))
        )


        # BOOKING PAGE


        with allure.step("Select boarding point"):
            booking_page.select_boarding_point()

        with allure.step("Select dropping point"):
            booking_page.select_dropping_point()

        with allure.step("Select available seat"):
            booking_page.select_available_seat()
            attach_screenshot(driver, "Seat Selected")

        with allure.step("Click continue"):
            booking_page.click_continue()


        # PASSENGER PAGE


        with allure.step("Skip insurance"):
            booking_page.click_no_insurance()



        with allure.step("Fill passenger details"):
            booking_page.fill_passenger_details(
                name="Aditya Pandey",
                age="23",
                email="aditya@gmail.com",
                mobile="9876543210",
                address="Patna Bihar",
                pincode="800001"
            )
            attach_screenshot(driver, "Passengers details filled")

        with allure.step("Select Male"):
            booking_page.select_male_gender()

        with allure.step("Confirm checkbox"):
            booking_page.click_confirm_checkbox()

        with allure.step("Select personal trip"):
            booking_page.select_personal()

        with allure.step("Click pay button"):
            booking_page.click_pay_button()

        with allure.step("Select Credit/Debit/ATM Card payment option"):
            payment_page.select_card_payment_option()
            attach_screenshot(driver, "Payment option selected")

        with allure.step("Verify Cards payment page is displayed"):
            assert payment_page.verify_cards_payment_page_loaded(), \
                "Cards payment page did not load."

            log.info("Cards payment page displayed successfully.")



        log.info("E2E TEST PASSED")