import allure
import pytest

from pages.modals_page import ModalsPage


@allure.epic("practice-automation.com")
@allure.feature("Modals")
class TestModalsPositive:

    @allure.title("Page opens and shows both modal triggers")
    @pytest.mark.positive
    def test_page_loads_with_triggers(self, driver):
        page = ModalsPage(driver).open()
        assert page.is_visible(page.SIMPLE_MODAL_TRIGGER)
        assert page.is_visible(page.FORM_MODAL_TRIGGER)

    @allure.title("Simple modal opens on click and shows its text")
    @pytest.mark.positive
    def test_simple_modal_opens(self, driver):
        page = ModalsPage(driver).open()
        page.open_simple_modal()
        with allure.step("Simple modal is visible with expected text"):
            assert page.is_simple_modal_open()

    @allure.title("Simple modal can be closed")
    @pytest.mark.positive
    def test_simple_modal_can_be_closed(self, driver):
        page = ModalsPage(driver).open()
        page.open_simple_modal()
        assert page.is_simple_modal_open()
        page.close_simple_modal()
        with allure.step("Simple modal is no longer visible"):
            assert page.is_invisible(page.SIMPLE_MODAL_TEXT)

    @allure.title("Form modal opens on click")
    @pytest.mark.positive
    def test_form_modal_opens(self, driver):
        page = ModalsPage(driver).open()
        page.open_form_modal()
        assert page.is_form_modal_open()

    @allure.title("Form modal accepts Name, Email and Message")
    @pytest.mark.positive
    def test_form_modal_accepts_input(self, driver):
        page = ModalsPage(driver).open()
        page.open_form_modal()
        page.fill_form(name="Nikita QA", email="nikita.qa@example.com", message="Hello there")
        assert page.get_attribute(page.NAME_INPUT, "value") == "Nikita QA"
        assert page.get_attribute(page.EMAIL_INPUT, "value") == "nikita.qa@example.com"
        assert page.get_attribute(page.MESSAGE_INPUT, "value") == "Hello there"

    @allure.title("Submitting the form with valid data shows a success message")
    @pytest.mark.positive
    def test_form_modal_valid_submit_shows_success(self, driver):
        page = ModalsPage(driver).open()
        page.open_form_modal()
        page.fill_form(name="Nikita QA", email="nikita.qa@example.com", message="Hello there")
        page.submit_form()
        with allure.step("Success message is shown"):
            assert page.is_success_message_shown()

    @allure.title("Form modal can be re-opened after being closed")
    @pytest.mark.positive
    def test_form_modal_reopen(self, driver):
        page = ModalsPage(driver).open()
        page.open_form_modal()
        assert page.is_form_modal_open()
        page.close_form_modal()
        page.open_form_modal()
        assert page.is_form_modal_open()

    @allure.title("Message field accepts a long piece of text")
    @pytest.mark.positive
    def test_message_field_accepts_long_text(self, driver):
        page = ModalsPage(driver).open()
        page.open_form_modal()
        long_message = "Selenium " * 50
        page.fill_form(name="Nikita QA", email="nikita.qa@example.com", message=long_message.strip())
        assert page.get_attribute(page.MESSAGE_INPUT, "value") == long_message.strip()


@allure.epic("practice-automation.com")
@allure.feature("Modals")
class TestModalsNegative:

    @allure.title("The Name field is flagged invalid by the browser when left empty")
    @pytest.mark.negative
    def test_submit_without_required_name(self, driver):
        # The site's own JS submits via AJAX without checking `required`
        # itself - the "Thank you" text shows up regardless of what was
        # typed, so it can't be used as a negative signal here. The
        # `required` attribute is still real, though: the browser's own
        # HTML5 constraint validation reports the field invalid, which is
        # what this test checks instead.
        page = ModalsPage(driver).open()
        page.open_form_modal()
        page.fill_form(name="", email="nikita.qa@example.com", message="Hello")
        with allure.step("Browser reports the empty Name field as invalid"):
            assert not page.is_field_valid(page.NAME_INPUT)

    @allure.title("The Email field is flagged invalid by the browser for a malformed address")
    @pytest.mark.negative
    def test_submit_with_invalid_email(self, driver):
        page = ModalsPage(driver).open()
        page.open_form_modal()
        page.fill_form(name="Nikita QA", email="not-an-email", message="Hello")
        with allure.step("Browser reports the malformed email as invalid"):
            assert not page.is_field_valid(page.EMAIL_INPUT)

    @allure.title("The Name field is flagged invalid by the browser when the form is left empty")
    @pytest.mark.negative
    def test_submit_empty_form(self, driver):
        page = ModalsPage(driver).open()
        page.open_form_modal()
        with allure.step("Browser reports the empty, required Name field as invalid"):
            assert not page.is_field_valid(page.NAME_INPUT)

    @allure.title("Simple modal's text is not visible before it is opened")
    @pytest.mark.negative
    def test_simple_modal_hidden_before_open(self, driver):
        page = ModalsPage(driver).open()
        with allure.step("Simple modal text is not shown until the trigger is clicked"):
            assert not page.is_visible(page.SIMPLE_MODAL_TEXT, timeout=2)
