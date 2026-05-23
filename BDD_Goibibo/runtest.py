import argparse
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
ALLURE_RESULTS = PROJECT_ROOT / "reports" / "allure-results"
ALLURE_REPORT = PROJECT_ROOT / "reports" / "allure-report"
SCREENSHOTS = PROJECT_ROOT / "reports" / "screenshots"
LOGS = PROJECT_ROOT / "logs"
RESULT_SUMMARY = PROJECT_ROOT / "reports" / "test_results.csv"
PRETTY_OUTPUT = PROJECT_ROOT / "pretty.output"


def clean_directory(path):
    path.mkdir(parents=True, exist_ok=True)
    for item in path.iterdir():
        if item.name == ".gitkeep":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def run_command(command, cwd):
    print("Running:", " ".join(str(part) for part in command))
    return subprocess.run(command, cwd=str(cwd), text=True)


def build_behave_command(args):
    command = [
        sys.executable,
        "-m",
        "behave",
        "-f",
        "allure_behave.formatter:AllureFormatter",
        "-o",
        str(ALLURE_RESULTS),
        "-f",
        "pretty",
    ]

    if args.tags:
        command.extend(["--tags", args.tags])

    command.extend(["-D", f"browser={args.browser}"])
    command.extend(["-D", f"headless={str(args.headless).lower()}"])
    command.extend(["-D", f"close_browser={str(not args.keep_browser).lower()}"])

    if args.chrome_version_main:
        command.extend(["-D", f"chrome_version_main={args.chrome_version_main}"])

    return command


def generate_allure_report():
    allure_bin = shutil.which("allure")
    if not allure_bin:
        print("Allure CLI was not found on PATH. Results are still saved in reports/allure-results.")
        print("Install Allure CLI or run: allure serve reports/allure-results")
        return 0

    command = [
        allure_bin,
        "generate",
        str(ALLURE_RESULTS),
        "--clean",
        "-o",
        str(ALLURE_REPORT),
    ]
    return run_command(command, PROJECT_ROOT).returncode


def parse_args():
    parser = argparse.ArgumentParser(description="Run Goibibo Behave BDD tests with Allure reporting.")
    parser.add_argument("--tags", help='Behave tag expression, for example: "@smoke" or "@positive and not @wip"')
    parser.add_argument("--browser", default="chrome", help="Browser name. Default: chrome")
    parser.add_argument("--headless", action="store_true", help="Run Chrome in headless mode")
    parser.add_argument("--keep-browser", action="store_true", help="Keep browser open after scenario")
    parser.add_argument("--chrome-version-main", help="Optional Chrome major version for undetected-chromedriver")
    parser.add_argument("--no-clean", action="store_true", help="Do not clean previous screenshots/allure results")
    parser.add_argument("--no-report", action="store_true", help="Skip Allure HTML report generation")
    return parser.parse_args()


def main():
    args = parse_args()

    for path in [ALLURE_RESULTS, ALLURE_REPORT, SCREENSHOTS, LOGS]:
        path.mkdir(parents=True, exist_ok=True)

    if not args.no_clean:
        clean_directory(ALLURE_RESULTS)
        clean_directory(SCREENSHOTS)
        for generated_file in [RESULT_SUMMARY, PRETTY_OUTPUT]:
            if generated_file.exists():
                generated_file.unlink()

    command = build_behave_command(args)
    test_result = run_command(command, PROJECT_ROOT)

    if PRETTY_OUTPUT.exists():
        PRETTY_OUTPUT.unlink()

    if not args.no_report:
        report_code = generate_allure_report()
        if report_code != 0:
            print("Allure report generation failed, but raw results may still be available.")

    return test_result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
