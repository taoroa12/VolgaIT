"""Page object for https://practice-automation.com/calendars/

The site uses a Jetpack ("Grunion") contact form for this exercise. The
date field's real markup (captured from DevTools) is:

    <input type="text" id="g1065-1-selectorenteradate"
           class="date jp-contact-form-date grunion-field" ...>

and the submit button shares the same "pushbutton-wide" class used by the
form-modal exercise, so both are targeted directly by id/class instead of
the earlier blind placeholder guess.
"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CalendarsPage(BasePage):
    URL = "https://practice-automation.com/calendars/"

    DATE_INPUT = (By.ID, "g1065-1-selectorenteradate")
    SUBMIT_BUTTON = (
        By.XPATH,
        "//button[contains(@class,'pushbutton-wide')] | //input[contains(@class,'pushbutton-wide')]",
    )
    SUCCESS_MESSAGE = (By.XPATH, "//*[contains(text(), 'Thank you for your response')]")
    VALIDATION_MESSAGE = (
        By.XPATH,
        "//*[contains(@class,'error') or contains(@class,'invalid') or contains(@class,'not-valid')]",
    )

    def enter_date(self, date_text: str):
        self.type_text(self.DATE_INPUT, date_text)
        return self

    def get_date_value(self) -> str:
        return self.get_attribute(self.DATE_INPUT, "value")

    def submit(self):
        self.click(self.SUBMIT_BUTTON)
        return self

    def is_success_message_shown(self) -> bool:
        return self.is_visible(self.SUCCESS_MESSAGE, timeout=5)

    def clear_date(self):
        self.find_visible(self.DATE_INPUT).clear()
        return self
