"""Page object for https://practice-automation.com/form-fields/

This is the "page with the form" from task item 5: it contains the
"Automation tools" list (Selenium, Playwright, Cypress, Appium, Katalon
Studio) and a Message textarea to fill with that list.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage


class FormFieldsPage(BasePage):
    URL = "https://practice-automation.com/form-fields/"

    # id first, label-based XPath as fallback (first match in document order
    # is always the main form: the site's hidden modal form sits at the bottom).
    NAME_INPUT = (By.XPATH, "//input[@id='name-input'] | //label[contains(., 'Name')]/following::input[1]")
    EMAIL_INPUT = (By.XPATH, "//input[@id='email'] | //label[normalize-space()='Email']/following::input[1]")
    MESSAGE_INPUT = (By.XPATH, "//textarea[@id='message'] | //label[normalize-space()='Message']/following::textarea[1]")
    SUBMIT_BUTTON = (By.XPATH, "//button[@id='submit-btn'] | //button[normalize-space()='Submit']")
    AUTOMATION_TOOLS_ITEMS = (By.XPATH, "//*[normalize-space(text())='Automation tools']/following::ul[1]/li")

    def get_automation_tools(self) -> list[str]:
        """Read the items of the 'Automation tools' list as plain text."""
        return self.get_texts(self.AUTOMATION_TOOLS_ITEMS)

    def fill_name(self, name: str):
        self.type_text_reliably(self.NAME_INPUT, name)
        return self

    def fill_email(self, email: str):
        self.type_text_reliably(self.EMAIL_INPUT, email)
        return self

    def fill_message(self, text: str):
        self.type_text_reliably(self.MESSAGE_INPUT, text)
        return self

    def get_message_value(self) -> str:
        return self.get_attribute(self.MESSAGE_INPUT, "value")

    def submit(self):
        self.click(self.SUBMIT_BUTTON)
        return self

    def accept_alert_if_present(self, timeout: int = 3) -> str | None:
        """The form reports the result through a JS alert; accept it and return its text."""
        try:
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        except TimeoutException:
            return None
        text = alert.text
        alert.accept()
        return text
