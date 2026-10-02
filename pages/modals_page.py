"""Page object for https://practice-automation.com/modals/

Real markup captured from DevTools:

    <input name="g1051-name" id="g1051-name" ...>
    <textarea name="g1051-message" id="contact-form-comment-g1051-message" ...></textarea>
    <input type="email" name="g1051-email" id="g1051-email" ...>
    <button type="submit" class="pushbutton-wide">Submit</button>
    <button type="button" class="pum-close popmake-close" aria-label="Close">x</button>

This is a Jetpack ("Grunion") contact form, not Contact Form 7 as originally
guessed (the "g1051-*" id/name prefix gives it away) - so fields are
targeted by their real `name` attributes instead of the `your-*` CF7
convention. Both modals (simple + form) are Popup Maker popups, which is
why they share a "pum-close popmake-close" close button; that popup is
scoped to `.pum-active` so the close click always hits the currently open
one.
"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ModalsPage(BasePage):
    URL = "https://practice-automation.com/modals/"

    # --- triggers ---
    SIMPLE_MODAL_TRIGGER = (By.XPATH, "//*[self::button or self::a][contains(., 'Simple Modal')]")
    FORM_MODAL_TRIGGER = (By.XPATH, "//*[self::button or self::a][contains(., 'Form Modal')]")

    # --- shared: Popup Maker close button, scoped to the active popup ---
    ACTIVE_MODAL_CLOSE = (By.CSS_SELECTOR, ".pum-active .pum-close.popmake-close")

    # --- simple modal ---
    SIMPLE_MODAL_TEXT = (
        By.XPATH,
        "//*[contains(text(), \"I'm a simple modal\") or contains(text(), 'I’m a simple modal')]",
    )
    SIMPLE_MODAL_CLOSE = ACTIVE_MODAL_CLOSE

    # --- form modal (Jetpack/Grunion contact form) ---
    NAME_INPUT = (By.NAME, "g1051-name")
    EMAIL_INPUT = (By.NAME, "g1051-email")
    MESSAGE_INPUT = (By.NAME, "g1051-message")
    FORM_SUBMIT_BUTTON = (By.CSS_SELECTOR, "button.pushbutton-wide")
    FORM_SUCCESS_MESSAGE = (By.XPATH, "//*[contains(text(), 'Thank you for your response')]")
    FORM_VALIDATION_TIP = (By.CSS_SELECTOR, ".wpcf7-not-valid-tip, .form-error, .error")
    FORM_MODAL_CLOSE = ACTIVE_MODAL_CLOSE

    # ---------- simple modal ----------
    def open_simple_modal(self):
        self.click(self.SIMPLE_MODAL_TRIGGER)
        return self

    def is_simple_modal_open(self) -> bool:
        return self.is_visible(self.SIMPLE_MODAL_TEXT, timeout=10)

    def close_simple_modal(self):
        self.click(self.SIMPLE_MODAL_CLOSE)
        # Popup Maker fades the popup out; wait until it is really gone so a
        # following click/open does not hit a popup that is still closing.
        self.is_invisible(self.SIMPLE_MODAL_TEXT, timeout=self.timeout)
        return self

    # ---------- form modal ----------
    def open_form_modal(self):
        self.click(self.FORM_MODAL_TRIGGER)
        return self

    def is_form_modal_open(self) -> bool:
        return self.is_visible(self.NAME_INPUT, timeout=10)

    def fill_form(self, name: str = "", email: str = "", message: str = ""):
        if name is not None:
            self.type_text_reliably(self.NAME_INPUT, name)
        if email is not None:
            self.type_text_reliably(self.EMAIL_INPUT, email)
        if message is not None:
            self.type_text_reliably(self.MESSAGE_INPUT, message)
        return self

    def submit_form(self):
        self.click(self.FORM_SUBMIT_BUTTON)
        return self

    def is_success_message_shown(self) -> bool:
        return self.is_visible(self.FORM_SUCCESS_MESSAGE, timeout=5)

    def get_validation_tips(self) -> list[str]:
        return self.get_texts(self.FORM_VALIDATION_TIP)

    def close_form_modal(self):
        self.click(self.FORM_MODAL_CLOSE)
        self.is_invisible(self.NAME_INPUT, timeout=self.timeout)
        return self
