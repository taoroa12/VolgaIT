"""Common Selenium helpers shared by all page objects (Page Object Model)."""
from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)

DEFAULT_TIMEOUT = 10


class BasePage:
    """Base class every concrete Page Object inherits from."""

    URL: str = ""  # overridden by subclasses

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    # ---------- navigation ----------
    def open(self):
        self.driver.get(self.URL)
        return self

    # ---------- element access ----------
    def find(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator: tuple[str, str]) -> list[WebElement]:
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def find_visible(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_clickable(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    # ---------- actions ----------
    def click(self, locator: tuple[str, str]):
        try:
            self.find_clickable(locator).click()
        except ElementClickInterceptedException:
            # fall back to a JS click, e.g. when an overlay/animation is in the way
            el = self.find(locator)
            self.driver.execute_script("arguments[0].click();", el)

    def type_text(self, locator: tuple[str, str], text: str, clear_first: bool = True):
        el = self.find_visible(locator)
        if clear_first:
            el.clear()
        el.send_keys(text)

    def get_text(self, locator: tuple[str, str]) -> str:
        return self.find_visible(locator).text.strip()

    def get_texts(self, locator: tuple[str, str]) -> list[str]:
        return [el.text.strip() for el in self.find_all(locator) if el.text.strip()]

    def get_attribute(self, locator: tuple[str, str], attr: str) -> str:
        return self.find(locator).get_attribute(attr)

    # ---------- state checks ----------
    def is_visible(self, locator: tuple[str, str], timeout: int | None = None) -> bool:
        try:
            WebDriverWait(self.driver, timeout or self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_invisible(self, locator: tuple[str, str], timeout: int | None = None) -> bool:
        try:
            WebDriverWait(self.driver, timeout or self.timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def exists(self, locator: tuple[str, str]) -> bool:
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def wait_for_text_present(self, locator: tuple[str, str], text: str, timeout: int | None = None) -> bool:
        try:
            WebDriverWait(self.driver, timeout or self.timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
            return True
        except TimeoutException:
            return False

    def is_field_valid(self, locator: tuple[str, str]) -> bool:
        """Browser-native HTML5 constraint-validation state (required/type=email/etc.)

        Useful for pages whose JS submits via AJAX without respecting a real
        form 'submit' event: the field can still be flagged invalid by the
        browser even though the site's own success text appears anyway.
        """
        el = self.find(locator)
        return bool(self.driver.execute_script("return arguments[0].checkValidity();", el))


# Locators that appear on (almost) every page of the site.
class CommonLocators:
    PAGE_HEADING = (By.TAG_NAME, "h1")
