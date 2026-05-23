import re
from datetime import datetime
from pathlib import Path

import allure

from utils.config_reader import config, PROJECT_ROOT
from utils.logger import LOG_FILE, get_logger


log = get_logger()


def safe_name(value):
    value = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(value)).strip("_")
    return value[:120] or "screenshot"


def screenshot_dir():
    rel_path = config.get("reports", "screenshots_dir", "reports/screenshots")
    path = PROJECT_ROOT / rel_path
    path.mkdir(parents=True, exist_ok=True)
    return path


def capture_screenshot(driver, name, attach=True, subfolder=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    base_dir = screenshot_dir()
    if subfolder:
        base_dir = base_dir / safe_name(subfolder)
        base_dir.mkdir(parents=True, exist_ok=True)

    file_path = base_dir / f"{timestamp}_{safe_name(name)}.png"
    driver.save_screenshot(str(file_path))
    log.info(f"Screenshot saved: {file_path}")

    if attach:
        allure.attach.file(
            str(file_path),
            name=safe_name(name),
            attachment_type=allure.attachment_type.PNG,
        )

    return file_path


def attach_execution_log(name="Execution Logs"):
    if LOG_FILE.exists():
        allure.attach.file(
            str(LOG_FILE),
            name=name,
            attachment_type=allure.attachment_type.TEXT,
        )

