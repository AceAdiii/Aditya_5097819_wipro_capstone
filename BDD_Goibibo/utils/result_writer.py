import csv
from datetime import datetime
from pathlib import Path

from utils.config_reader import PROJECT_ROOT


RESULT_FILE = PROJECT_ROOT / "reports" / "test_results.csv"


def append_result(scenario):
    RESULT_FILE.parent.mkdir(parents=True, exist_ok=True)
    new_file = not RESULT_FILE.exists()

    with RESULT_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if new_file:
            writer.writerow(["timestamp", "scenario", "status", "tags"])
        writer.writerow(
            [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                scenario.name,
                str(scenario.status).split(".")[-1].upper(),
                ",".join(scenario.tags),
            ]
        )

