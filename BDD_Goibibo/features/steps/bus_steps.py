from behave import given, then, when
from selenium.common.exceptions import NoSuchWindowException, WebDriverException

from locators.home_locators import HomeLocators


@given("the Goibibo bus module is open")
def step_open_bus_module(context):
    try:
        context.home_page.open_bus_module()
    except NoSuchWindowException:
        context.restart_browser()
        context.home_page.open_bus_module()
    except WebDriverException as error:
        message = str(error).lower()
        if "no such window" not in message and "web view not found" not in message:
            raise
        context.restart_browser()
        context.home_page.open_bus_module()


@when('I search buses from "{source}" to "{destination}"')
def step_search_buses(context, source, destination):
    context.home_page.search_buses(source, destination)
    context.search_page.wait_for_results()


@when('I enter bus source "{source}" and destination "{destination}"')
def step_enter_source_and_destination(context, source, destination):
    context.home_page.enter_source_city(source)
    context.home_page.enter_destination_city(destination)


@when("I leave the bus source empty")
def step_leave_source_empty(context):
    source = context.home_page.find_visible(HomeLocators.SOURCE_CITY_INPUT, timeout=15)
    source.clear()
    context.log.info("Source city left empty.")


@when('I enter bus destination "{destination}"')
def step_enter_destination_only(context, destination):
    context.home_page.enter_destination_city(destination)


@when("I click the Search Bus button")
def step_click_search_button(context):
    context.home_page.click_search_button()


@then("bus search results should be displayed")
def step_results_should_display(context):
    assert context.search_page.verify_results_displayed(), "Bus results page did not load."


@then("bus search results should not be displayed")
def step_results_should_not_display(context):
    assert not context.search_page.verify_results_displayed(timeout=7), (
        "Bus results loaded even though the search inputs were invalid."
    )


@then("the same-city validation message should be displayed")
def step_same_city_validation(context):
    message = context.home_page.same_city_error_message()
    assert "Source and Destination can't be same" in message, (
        f"Expected same-city validation message, but got: {message}"
    )


@when("I apply the AC bus filter")
def step_apply_ac_filter(context):
    context.search_page.click_ac_filter()


@when("I apply the Sleeper bus filter")
def step_apply_sleeper_filter(context):
    context.search_page.click_sleeper_filter()


@when("I sort the bus results by price")
def step_sort_by_price(context):
    context.search_page.sort_by_price()


@when("I sort the bus results by duration")
def step_sort_by_duration(context):
    context.search_page.sort_by_duration()


@then("at least one bus result should be visible")
def step_at_least_one_bus_result(context):
    count = context.search_page.get_bus_count()
    assert count > 0, "Expected at least one visible bus result."


@then("bus results should be sorted by lowest price first")
def step_results_sorted_by_price(context):
    prices = context.search_page.get_visible_prices()
    assert len(prices) >= 2, f"Expected at least two visible prices to verify sorting, got: {prices}"
    assert prices == sorted(prices), f"Expected prices to be sorted low to high, got: {prices}"


@then("bus results should be sorted by shortest duration first")
def step_results_sorted_by_duration(context):
    durations = context.search_page.get_visible_durations()
    assert len(durations) >= 2, f"Expected at least two visible durations to verify sorting, got: {durations}"
    assert durations == sorted(durations), (
        f"Expected durations to be sorted shortest to longest, got minutes: {durations}"
    )


@when("I choose a bus and open seat selection")
def step_open_seat_selection(context):
    context.search_page.open_seat_selection(bus_index=0)


@when("I select boarding point, dropping point, and one available seat")
def step_select_points_and_seat(context):
    context.booking_page.select_first_boarding_dropping_and_seat()


@when("I continue to traveller details")
def step_continue_to_traveller_details(context):
    context.booking_page.click_continue()


@when("I skip travel insurance")
def step_skip_insurance(context):
    context.booking_page.skip_insurance()


@when("I enter passenger details")
def step_enter_passenger_details(context):
    row = context.table[0].as_dict()
    context.booking_page.fill_passenger_details(
        name=row["name"],
        age=row["age"],
        email=row["email"],
        mobile=row["mobile"],
        address=row["address"],
        pincode=row["pincode"],
    )


@when("I confirm billing details and choose personal trip")
def step_confirm_billing_and_trip(context):
    context.booking_page.confirm_billing_and_personal_trip()


@when("I proceed to payment")
def step_proceed_to_payment(context):
    context.booking_page.click_pay_button()


@when("I select card payment option")
def step_select_card_payment(context):
    context.payment_page.select_card_payment_option()


@then("the card payment page should be displayed")
def step_card_payment_displayed(context):
    assert context.payment_page.is_card_payment_page_loaded(), "Card payment form did not load."

