import shutil
import sys
from pathlib import Path

import allure
from selenium.common.exceptions import NoSuchWindowException, WebDriverException

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pages.bus_booking_page import BusBookingPage
from pages.bus_search_page import BusSearchPage
from pages.home_page import HomePage
from pages.payment_page import PaymentPage
from utils.config_reader import config
from utils.driver_factory import create_driver
from utils.logger import LOG_FILE, get_logger
from utils.result_writer import append_result
from utils.screenshot_utils import attach_execution_log, capture_screenshot


def _clean_runtime_artifacts():
    for rel_path in [
        config.get("reports", "screenshots_dir", "reports/screenshots"),
        config.get("reports", "allure_results_dir", "reports/allure-results"),
    ]:
        path = PROJECT_ROOT / rel_path
        path.mkdir(parents=True, exist_ok=True)

    (PROJECT_ROOT / config.get("reports", "logs_dir", "logs")).mkdir(parents=True, exist_ok=True)


def _userdata_bool(context, key, fallback):
    value = context.config.userdata.get(key)
    if value is None:
        return fallback
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _is_browser_open(driver):
    if not driver:
        return False
    try:
        driver.current_window_handle
        return True
    except (NoSuchWindowException, WebDriverException):
        return False


def _build_page_objects(context):
    context.home_page = HomePage(context.driver)
    context.search_page = BusSearchPage(context.driver)
    context.booking_page = BusBookingPage(context.driver)
    context.payment_page = PaymentPage(context.driver)


def _start_browser(context):
    context.driver = create_driver(context.config.userdata)
    _build_page_objects(context)


def _stop_browser(context):
    driver = getattr(context, "driver", None)
    if not driver:
        return

    try:
        driver.quit()
    except Exception as error:
        context.log.info(f"Browser was already closed: {error.__class__.__name__}")
    finally:
        try:
            driver.quit = lambda *args, **kwargs: None
        except Exception:
            pass
        context.driver = None


def _restart_browser(context):
    context.log.warning("Browser window closed unexpectedly. Restarting browser for this scenario.")
    _stop_browser(context)
    _start_browser(context)


def before_all(context):
    _clean_runtime_artifacts()
    context.project_root = PROJECT_ROOT
    context.log = get_logger()
    context.log.info("========== BDD TEST RUN STARTED ==========")

    allure_results_dir = PROJECT_ROOT / config.get("reports", "allure_results_dir", "reports/allure-results")
    allure_results_dir.mkdir(parents=True, exist_ok=True)
    environment_file = allure_results_dir / "environment.properties"
    environment_file.write_text(
        "\n".join(
            [
                "Project=BDD_Goibibo",
                f"Base_URL={config.get('basic info', 'url')}",
                f"Bus_URL={config.get('basic info', 'bus_url')}",
                f"Browser={context.config.userdata.get('browser', config.get('basic info', 'browser'))}",
                f"Headless={context.config.userdata.get('headless', config.get('basic info', 'headless'))}",
            ]
        ),
        encoding="utf-8",
    )


def before_scenario(context, scenario):
    context.log.info(f"========== STARTING SCENARIO: {scenario.name} ==========")
    _start_browser(context)
    context.restart_browser = lambda: _restart_browser(context)


def after_step(context, step):
    driver = getattr(context, "driver", None)
    if not driver:
        return

    should_attach = config.get_bool("reports", "attach_step_screenshots", True)
    should_save = config.get_bool("reports", "save_step_screenshots", True)
    if not should_attach and not should_save:
        return

    status = str(step.status).split(".")[-1].upper()
    scenario_name = getattr(getattr(context, "scenario", None), "name", "scenario")
    screenshot_name = f"{status}_{step.keyword.strip()}_{step.name}"

    try:
        capture_screenshot(
            driver,
            screenshot_name,
            attach=should_attach,
            subfolder=scenario_name if should_save else None,
        )
    except Exception as error:
        context.log.warning(f"Unable to capture screenshot for step '{step.name}': {error}")

    if status == "FAILED":
        attach_execution_log()


def after_scenario(context, scenario):
    driver = getattr(context, "driver", None)

    if _is_browser_open(driver):
        try:
            capture_screenshot(
                driver,
                f"FINAL_{str(scenario.status).split('.')[-1].upper()}_{scenario.name}",
                attach=True,
                subfolder=scenario.name,
            )
        except Exception as error:
            context.log.warning(f"Unable to capture final screenshot: {error}")

    attach_execution_log()
    append_result(scenario)

    close_browser = _userdata_bool(
        context,
        "close_browser",
        config.get_bool("basic info", "close_browser", True),
    )
    if driver and close_browser:
        context.log.info("Closing browser.")
        _stop_browser(context)

    context.log.info(f"========== FINISHED SCENARIO: {scenario.name} | {scenario.status} ==========")


def after_all(context):
    context.log.info("========== BDD TEST RUN FINISHED ==========")
    if LOG_FILE.exists():
        # Keep a latest copy inside reports for easy submission with Allure artifacts.
        reports_log = PROJECT_ROOT / "reports" / "execution.log"
        shutil.copyfile(LOG_FILE, reports_log)
