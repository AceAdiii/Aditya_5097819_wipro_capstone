from selenium import webdriver
from selenium.webdriver.chrome.options import Options as SeleniumChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
import winreg

from utils.config_reader import config
from utils.logger import get_logger


log = get_logger()


def _as_bool(value):
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _build_chrome_options(headless=False, undetected=True):
    options = uc.ChromeOptions() if undetected else SeleniumChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--lang=en-US")

    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    return options


def _detect_chrome_major_version():
    registry_paths = [
        (winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Google\Chrome\BLBeacon"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Google\Chrome\BLBeacon"),
    ]

    for hive, path in registry_paths:
        try:
            with winreg.OpenKey(hive, path) as key:
                version, _ = winreg.QueryValueEx(key, "version")
                return int(str(version).split(".")[0])
        except Exception:
            continue

    return None


def create_driver(userdata=None):
    userdata = userdata or {}
    browser = userdata.get("browser", config.get("basic info", "browser", "chrome"))
    headless_value = userdata.get("headless", config.get("basic info", "headless", "false"))
    headless = _as_bool(headless_value)

    if browser.lower() != "chrome":
        raise ValueError("This project is configured for Chrome because Goibibo blocks many generic drivers.")

    version_main = userdata.get(
        "chrome_version_main",
        config.get("basic info", "chrome_version_main", "auto"),
    )
    version_main = str(version_main).strip()
    detected_version = _detect_chrome_major_version() if version_main.lower() == "auto" else None

    try:
        log.info("Launching Chrome with undetected-chromedriver.")
        uc_options = _build_chrome_options(headless=headless, undetected=True)
        kwargs = {"options": uc_options}
        if version_main and version_main.lower() != "auto":
            kwargs["version_main"] = int(version_main)
        elif detected_version:
            kwargs["version_main"] = detected_version
        driver = uc.Chrome(**kwargs)
    except Exception as error:
        log.warning(f"undetected-chromedriver launch failed, falling back to Selenium Chrome. Error: {error}")
        selenium_options = _build_chrome_options(headless=headless, undetected=False)
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=selenium_options)

    driver.implicitly_wait(config.get_int("basic info", "implicit_wait", 0))
    driver.set_page_load_timeout(config.get_int("basic info", "page_load_timeout", 70))
    return driver
