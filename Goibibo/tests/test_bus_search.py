import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.home_page import HomePage
from pages.bus_search_page import BusSearchPage
from utilities.logger import get_logger

log = get_logger()



# SHARED HELPER


def _navigate_to_results(driver, source="Delhi", destination="Lucknow"):
    """
    Open homepage → close popups → Bus tab → fill form → search.
    Returns BusSearchPage object after results load.
    """

    driver.get("https://www.goibibo.com/")

    home = HomePage(driver)

    home.close_popup()
    home.close_login_popup()

    home.click_bus_button()

    home.enter_source_city(source)
    home.enter_destination_city(destination)

    home.click_search_button()

    search_page = BusSearchPage(driver)

    assert search_page.verify_bus_results_displayed(), \
        "Pre-condition FAILED – bus results page did not load."

    return search_page



# TEST CLASS


@allure.feature("Bus Search Module")
class TestBusSearch:


    #                           POSITIVE TEST CASES



    #                           TC-P01  Search with Valid Data

    @allure.story("Search buses with valid data")
    @allure.title("TC-P01 | Valid search – Delhi to Lucknow should return results")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description(
        "Navigate to the Bus tab, enter valid source (Delhi) and destination "
        "(Lucknow), click Search Bus, and verify that the results page loads "
        "with the Filters panel visible."
    )
    def test_search_bus_valid_data(self, setup):
        driver = setup
        home_page = HomePage(driver)

        with allure.step("Close login and popup dialogs"):
            log.info("TC-P01 | Attempting to close popup.")
            home_page.close_popup()
            log.info("TC-P01 | Attempting to close login popup.")
            home_page.close_login_popup()

        with allure.step("Navigate to Bus section"):
            log.info("TC-P01 | Clicking on Bus button.")
            home_page.click_bus_button()

        with allure.step("Enter source city: Delhi"):
            log.info("TC-P01 | Entering source city: Delhi.")
            home_page.enter_source_city("Delhi")

        with allure.step("Enter destination city: Lucknow"):
            log.info("TC-P01 | Entering destination city: Lucknow.")
            home_page.enter_destination_city("Lucknow")

        with allure.step("Click Search Bus button"):
            log.info("TC-P01 | Clicking search button.")
            home_page.click_search_button()

        with allure.step("Verify bus search results are displayed"):
            bus_search_page = BusSearchPage(driver)
            log.info("TC-P01 | Validating bus search results are displayed.")
            assert bus_search_page.verify_bus_results_displayed(), \
                "TC-P01 FAILED – Bus results page did not load."
            log.info("TC-P01 PASSED.")


    #                           TC-P02  Apply AC Filter

    @allure.story("Filter: AC Buses")
    @allure.title("TC-P02 | Apply AC filter – buses should remain visible")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "After searching Delhi to Lucknow, apply the AC filter chip and "
        "verify that bus result cards are still displayed on the page."
    )
    def test_apply_ac_filter(self, setup):
        driver = setup

        with allure.step("Search buses from Delhi to Lucknow"):
            log.info("TC-P02 | Searching Delhi to Lucknow.")
            search_page = _navigate_to_results(driver)

        with allure.step("Click AC filter chip"):
            log.info("TC-P02 | Clicking AC filter.")
            search_page.click_ac_filter()

        with allure.step("Verify bus cards are still displayed after AC filter"):
            log.info("TC-P02 | Verifying AC filtered results.")
            bus_search_page = BusSearchPage(driver)
            assert bus_search_page.verify_bus_results_displayed(), \
                "TC-P02 FAILED – No bus cards visible after applying AC filter."
            log.info("TC-P02 PASSED.")


    #                         TC-P03  Apply Sleeper Filter

    @allure.story("Filter: Sleeper Buses")
    @allure.title("TC-P03 | Apply Sleeper filter – results should remain visible")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "After searching Delhi to Lucknow, apply the Sleeper filter chip "
        "and verify that the results section is still displayed."
    )
    def test_apply_sleeper_filter(self, setup):
        driver = setup

        with allure.step("Search buses from Delhi to Lucknow"):
            log.info("TC-P03 | Searching Delhi to Lucknow.")
            search_page = _navigate_to_results(driver)

        with allure.step("Click Sleeper filter chip"):
            log.info("TC-P03 | Clicking Sleeper filter.")
            search_page.click_sleeper_filter()

        with allure.step("Verify results are still shown after Sleeper filter"):
            results_visible = search_page.verify_bus_results_displayed()
            log.info(f"TC-P03 | Results visible: {results_visible}")
            assert results_visible, \
                "TC-P03 FAILED – Results section not visible after Sleeper filter."
            log.info("TC-P03 PASSED.")


    #                             TC-P04  Sort by Price

    @allure.story("Sort: By Price")
    @allure.title("TC-P04 | Sort results by Price – page should be stable")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description(
        "After searching Delhi to Lucknow, click the 'Price' sort option "
        "and verify the results page is still loaded and showing bus cards."
    )
    def test_sort_by_price(self, setup):
        driver = setup

        with allure.step("Search buses from Delhi to Lucknow"):
            log.info("TC-P04 | Searching Delhi to Lucknow.")
            search_page = _navigate_to_results(driver)

        with allure.step("Apply sort by Price"):
            log.info("TC-P04 | Sorting by Price.")
            search_page.sort_by_price()

        with allure.step("Verify results are displayed after price sort"):
            count = search_page.get_bus_count()
            log.info(f"TC-P04 | Bus cards after price sort: {count}")
            assert count > 0, \
                "TC-P04 FAILED – No bus cards found after sorting by price."
            log.info("TC-P04 PASSED.")


    #                            TC-P05  Sort by Duration

    @allure.story("Sort: By Duration")
    @allure.title("TC-P05 | Sort results by Duration – page should be stable")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description(
        "After searching Delhi to Lucknow, click the 'Duration' sort option "
        "and verify the results page remains stable with bus cards visible."
    )
    def test_sort_by_duration(self, setup):
        driver = setup

        with allure.step("Search buses from Delhi to Lucknow"):
            log.info("TC-P05 | Searching Delhi to Lucknow.")
            search_page = _navigate_to_results(driver)

        with allure.step("Apply sort by Duration"):
            log.info("TC-P05 | Sorting by Duration.")
            search_page.sort_by_duration()

        with allure.step("Verify results are displayed after duration sort"):
            count = search_page.get_bus_count()
            log.info(f"TC-P05 | Bus cards after duration sort: {count}")
            assert count > 0, \
                "TC-P05 FAILED – No bus cards found after sorting by duration."
            log.info("TC-P05 PASSED.")


    #                          NEGATIVE TEST CASES



    #                      TC-N01  Same Source and Destination

    @allure.story("Negative: Same source and destination city")
    @allure.title("TC-N01 | Same source & destination – valid results must NOT appear")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Enter 'Delhi' as both source and destination and attempt to search. "
        "The application should show validation message."
    )
    def test_same_source_and_destination(self, setup):

        driver = setup
        home_page = HomePage(driver)

        with allure.step("Close popups and navigate to Bus tab"):
            log.info("TC-N01 | Closing popups.")
            home_page.close_popup()
            home_page.close_login_popup()
            home_page.click_bus_button()

        with allure.step("Enter 'Delhi' as source city"):
            log.info("TC-N01 | Entering Delhi as source.")
            home_page.enter_source_city("Delhi")

        with allure.step("Enter 'Delhi' as destination city"):
            log.info("TC-N01 | Entering Delhi as destination.")
            home_page.enter_destination_city("Delhi")

        with allure.step("Click Search Bus"):
            log.info("TC-N01 | Clicking search button.")
            home_page.click_search_button()

        with allure.step("Verify error message is displayed"):
            error_msg = home_page.get_same_city_error_message()

            assert "Source and Destination can't be same" in error_msg, \
                "TC-N01 FAILED – Expected validation message not displayed."

            log.info("TC-N01 PASSED.")


    #                       TC-N02  Empty Source City

    @allure.story("Negative: Search with empty source city")
    @allure.title("TC-N02 | Empty source city – search should not proceed")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_empty_source_city(self, setup):

        driver = setup

        home_page = HomePage(driver)

        with allure.step("Close popups and navigate to Bus tab"):

            log.info("TC-N02 | Closing popups.")

            home_page.close_popup()
            home_page.close_login_popup()
            home_page.click_bus_button()

        with allure.step("Leave source city blank"):

            log.info("TC-N02 | Source city intentionally left empty.")

        with allure.step("Enter destination city – Lucknow"):

            log.info("TC-N02 | Entering destination: Lucknow.")

            home_page.enter_destination_city("Lucknow")

        with allure.step("Click Search Bus with empty source"):

            log.info("TC-N02 | Clicking Search Bus.")

            home_page.click_search_button()

        with allure.step("Verify results page has NOT loaded"):

            try:
                filter_present = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//span[contains(text(),'Filters')]")
                    )
                ).is_displayed()

            except Exception:
                filter_present = False

            assert not filter_present, \
                "TC-N02 FAILED – Results page loaded even with empty source city."

            log.info("TC-N02 PASSED.")