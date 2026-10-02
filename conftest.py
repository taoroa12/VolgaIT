import os
import platform

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", choices=["chrome", "firefox"],
        help="Browser to run the UI tests in.",
    )
    parser.addoption(
        "--headless", action="store_true", default=False,
        help="Run the browser in headless mode.",
    )


@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless") or os.getenv("CI") == "true"

    if browser == "firefox":
        options = FirefoxOptions()
        options.page_load_strategy = "eager"
        if headless:
            options.add_argument("--headless")
        drv = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    else:
        options = ChromeOptions()
        options.page_load_strategy = "eager"  # don't wait for ads/analytics: slow networks made get() hang
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1400,1000")
        options.add_argument("--disable-notifications")
        drv = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    drv.set_page_load_timeout(60)
    drv.implicitly_wait(0)  # explicit waits only, see pages/base_page.py
    drv.maximize_window()
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the Allure report whenever a test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"screenshot_on_failure_{item.name}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass


def pytest_sessionfinish(session, exitstatus):
    """Fill the 'Environment' block of the Allure report."""
    results_dir = getattr(session.config.option, "allure_report_dir", None)
    if not results_dir:
        return
    os.makedirs(results_dir, exist_ok=True)
    lines = [
        f"Browser={session.config.getoption('--browser')}",
        f"Headless={session.config.getoption('--headless')}",
        f"Python={platform.python_version()}",
        f"OS={platform.system()} {platform.release()}",
        "Base_URL=https://practice-automation.com/",
    ]
    with open(os.path.join(results_dir, "environment.properties"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
