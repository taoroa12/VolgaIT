"""Tests for https://practice-automation.com/calendars/

Test data intentionally covers: a "normal" date, a leap-year edge case,
today's date, a far-future/far-past date, and negative/garbage input.
"""
import datetime

import allure
import pytest

from pages.calendars_page import CalendarsPage

TODAY = datetime.date.today().isoformat()


@allure.epic("practice-automation.com")
@allure.feature("Calendars")
class TestCalendarsPositive:

    @allure.title("Page opens and shows the date field and Submit button")
    @pytest.mark.positive
    def test_page_loads_with_expected_controls(self, driver):
        page = CalendarsPage(driver).open()
        with allure.step("Date input and Submit button are visible"):
            assert page.is_visible(page.DATE_INPUT)
            assert page.is_visible(page.SUBMIT_BUTTON)

    @allure.title("A valid ISO date can be typed into the field")
    @pytest.mark.positive
    def test_valid_date_is_accepted(self, driver):
        page = CalendarsPage(driver).open()
        with allure.step("Type a valid date"):
            page.enter_date("2026-05-15")
        with allure.step("Field reflects the typed value"):
            assert page.get_date_value() == "2026-05-15"

    @allure.title("Submitting a valid date shows the success message")
    @pytest.mark.positive
    def test_submit_valid_date_shows_success(self, driver):
        page = CalendarsPage(driver).open()
        page.enter_date("2026-05-15").submit()
        with allure.step("Success message is shown"):
            assert page.is_success_message_shown()

    @allure.title("Today's date is accepted")
    @pytest.mark.positive
    def test_todays_date_is_accepted(self, driver):
        page = CalendarsPage(driver).open()
        page.enter_date(TODAY)
        assert page.get_date_value() == TODAY

    @allure.title("Leap-year date (2024-02-29) is accepted")
    @pytest.mark.positive
    def test_leap_year_date_is_accepted(self, driver):
        page = CalendarsPage(driver).open()
        page.enter_date("2024-02-29")
        assert page.get_date_value() == "2024-02-29"

    @allure.title("A far-future date is accepted")
    @pytest.mark.positive
    def test_far_future_date_is_accepted(self, driver):
        page = CalendarsPage(driver).open()
        page.enter_date("2099-12-31")
        assert page.get_date_value() == "2099-12-31"

    @allure.title("A far-past date is accepted")
    @pytest.mark.positive
    def test_far_past_date_is_accepted(self, driver):
        page = CalendarsPage(driver).open()
        page.enter_date("1970-01-01")
        assert page.get_date_value() == "1970-01-01"

    @allure.title("The field can be cleared and re-filled")
    @pytest.mark.positive
    def test_field_can_be_cleared_and_refilled(self, driver):
        page = CalendarsPage(driver).open()
        page.enter_date("2026-01-01")
        page.clear_date()
        assert page.get_date_value() == ""
        page.enter_date("2026-02-02")
        assert page.get_date_value() == "2026-02-02"

    @allure.title("Re-submitting after changing the date updates the result")
    @pytest.mark.positive
    def test_resubmit_after_changing_date(self, driver):
        page = CalendarsPage(driver).open()
        page.enter_date("2026-03-03").submit()
        assert page.is_success_message_shown()
        # A successful AJAX submit swaps the form for the "thank you" state,
        # so the date field is gone until the page is freshly loaded again.
        page.open()
        page.enter_date("2026-04-04").submit()
        assert page.is_success_message_shown()


@allure.epic("practice-automation.com")
@allure.feature("Calendars")
class TestCalendarsNegative:

    @allure.title("Submitting with an empty date field does not show success")
    @pytest.mark.negative
    def test_submit_without_date(self, driver):
        page = CalendarsPage(driver).open()
        page.submit()
        with allure.step("Success message must not appear for empty input"):
            assert not page.is_success_message_shown()

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "bad_value",
        ["not-a-date", "2026-13-40", "99/99/9999"],
        ids=["free-text", "invalid-month-day", "invalid-format"],
    )
    @allure.title("Submitting a malformed date does not show success")
    def test_submit_invalid_date_formats(self, driver, bad_value):
        page = CalendarsPage(driver).open()
        page.enter_date(bad_value).submit()
        with allure.step(f"Success message must not appear for '{bad_value}'"):
            assert not page.is_success_message_shown()

    @allure.title("Whitespace-only input is not treated as a valid date")
    @pytest.mark.negative
    def test_submit_whitespace_only(self, driver):
        page = CalendarsPage(driver).open()
        page.enter_date("   ").submit()
        assert not page.is_success_message_shown()
