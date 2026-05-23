import time
import re

from selenium.common.exceptions import TimeoutException

from locators.bus_search_locators import BusSearchLocators
from pages.base_page import BasePage


class BusSearchPage(BasePage):
    def verify_results_displayed(self, timeout=35):
        self.log.info("Verifying bus search results are displayed.")
        try:
            self.find_visible(BusSearchLocators.FILTERS_TEXT, timeout=timeout)
            return self.get_bus_count(timeout=8) > 0
        except Exception as error:
            self.log.info(f"Bus results are not visible: {error.__class__.__name__}")
            return False

    def wait_for_results(self):
        if not self.verify_results_displayed(timeout=40):
            raise AssertionError("Bus search results page did not load.")

    def get_bus_count(self, timeout=10):
        try:
            cards = self.visible_elements(BusSearchLocators.BUS_CARDS, timeout=timeout)
            return len(cards)
        except Exception:
            buttons = [button for button in self.driver.find_elements(*BusSearchLocators.SELECT_SEAT_BUTTONS) if button.is_displayed()]
            return len(buttons)

    def get_visible_prices(self, limit=8):
        card_texts = self._visible_bus_card_texts(limit=limit)
        prices = []

        for text in card_texts:
            matches = re.findall(r"₹\s*([\d,]+)", text)
            if matches:
                prices.append(int(matches[0].replace(",", "")))

        return prices

    def get_visible_durations(self, limit=8):
        card_texts = self._visible_bus_card_texts(limit=limit)
        durations = []

        for text in card_texts:
            match = re.search(r"(\d+)\s*h(?:\s*(\d+)\s*m)?", text, flags=re.IGNORECASE)
            if match:
                hours = int(match.group(1))
                minutes = int(match.group(2) or 0)
                durations.append((hours * 60) + minutes)

        return durations

    def are_prices_sorted_low_to_high(self):
        prices = self.get_visible_prices()
        self.log.info(f"Visible bus prices after sorting: {prices}")
        return len(prices) >= 2 and prices == sorted(prices)

    def are_durations_sorted_low_to_high(self):
        durations = self.get_visible_durations()
        self.log.info(f"Visible bus durations after sorting: {durations}")
        return len(durations) >= 2 and durations == sorted(durations)

    def _visible_bus_card_texts(self, limit=8):
        self.find_visible(BusSearchLocators.FILTERS_TEXT, timeout=20)
        return self.driver.execute_script(
            """
            const limit = arguments[0];
            const visible = (el) => {
                const rect = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                return rect.width > 0 && rect.height > 0 &&
                       style.visibility !== 'hidden' &&
                       style.display !== 'none';
            };

            return Array.from(document.querySelectorAll(
                "div[class*='SrpActiveCardstyles__ActivecardLayoutDiv']"
            ))
                .filter(visible)
                .slice(0, limit)
                .map((card) => (card.innerText || card.textContent || '').replace(/\\s+/g, ' ').trim());
            """,
            limit,
        )

    def click_ac_filter(self):
        self.log.info("Applying AC filter.")
        self.click(BusSearchLocators.AC_FILTER, timeout=15)
        time.sleep(2)

    def click_sleeper_filter(self):
        self.log.info("Applying Sleeper filter.")
        self.click(BusSearchLocators.SLEEPER_FILTER, timeout=15)
        time.sleep(2)

    def sort_by_price(self):
        self.log.info("Sorting by cheapest price.")
        self._click_sort_label("CHEAPEST", "PRICE")

    def sort_by_duration(self):
        self.log.info("Sorting by fastest duration.")
        self._click_sort_label("FASTEST", "DURATION")

    def _click_sort_label(self, *labels: str):
        self.find_visible(BusSearchLocators.FILTERS_TEXT, timeout=20)
        labels = [label.upper() for label in labels]
        end_time = time.time() + 20

        while time.time() < end_time:
            clicked = self.driver.execute_script(
                """
                const labels = arguments[0];
                const visible = (el) => {
                    const rect = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);
                    return rect.width > 0 && rect.height > 0 &&
                           style.visibility !== 'hidden' &&
                           style.display !== 'none';
                };
                const textOf = (el) => (el.innerText || el.textContent || '')
                    .replace(/\\s+/g, ' ')
                    .trim()
                    .toUpperCase();

                const candidates = Array.from(
                    document.querySelectorAll('button, span, p, div, li')
                ).filter(visible);

                const target = candidates.find((el) => labels.includes(textOf(el)));
                if (!target) {
                    return false;
                }
                target.scrollIntoView({block: 'center', inline: 'center'});
                target.click();
                return true;
                """,
                labels,
            )
            if clicked:
                time.sleep(2)
                return
            time.sleep(0.5)

        raise AssertionError(f"Unable to click sort option with labels: {', '.join(labels)}")

    def open_seat_selection(self, bus_index=1):
        self.wait_for_results()
        buttons = self.visible_elements(BusSearchLocators.SELECT_SEAT_BUTTONS, timeout=20)

        if not buttons and self.is_visible(BusSearchLocators.SHOW_BUSES_BUTTON, timeout=4):
            self.click(BusSearchLocators.SHOW_BUSES_BUTTON, timeout=8)
            time.sleep(2)
            buttons = self.visible_elements(BusSearchLocators.SELECT_SEAT_BUTTONS, timeout=20)

        if not buttons:
            raise AssertionError("No SELECT SEAT buttons are available on results page.")

        selected_index = min(bus_index, len(buttons) - 1)
        self.log.info(f"Opening seat selection for bus button index: {selected_index}")
        self.scroll_to(buttons[selected_index])
        self.driver.execute_script("arguments[0].click();", buttons[selected_index])

        try:
            self.find_visible(BusSearchLocators.HIDE_SEAT_BUTTON, timeout=20)
        except TimeoutException:
            self.log.info("HIDE SEAT button did not appear, checking booking section directly.")
