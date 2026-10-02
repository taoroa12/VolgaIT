import allure
import pytest

from pages.ads_page import AdsPage
from pages.base_page import CommonLocators


@allure.epic("practice-automation.com")
@allure.feature("Ads")
class TestAdsPositive:

    @allure.title("Page opens and shows the ad instructions")
    @pytest.mark.positive
    def test_page_loads(self, driver):
        page = AdsPage(driver).open()
        with allure.step("Page heading is visible"):
            assert page.is_visible(CommonLocators.PAGE_HEADING)

    @allure.title("The ad modal appears automatically after the countdown")
    @pytest.mark.positive
    def test_ad_appears_automatically(self, driver):
        page = AdsPage(driver).open()
        with allure.step("Ad modal becomes visible within the expected countdown window"):
            assert page.wait_for_ad_to_appear()

    @allure.title("The ad modal shows the expected text")
    @pytest.mark.positive
    def test_ad_shows_expected_text(self, driver):
        page = AdsPage(driver).open()
        page.wait_for_ad_to_appear()
        with allure.step("Ad text matches 'I am an ad.'"):
            assert page.get_text(page.AD_MODAL_TEXT) == "I am an ad."

    @allure.title("The ad modal can be closed")
    @pytest.mark.positive
    def test_ad_can_be_closed(self, driver):
        page = AdsPage(driver).open()
        page.wait_for_ad_to_appear()
        page.close_ad()
        with allure.step("Ad modal is no longer visible after closing"):
            assert page.is_ad_closed()

    @allure.title("Reloading the page shows the ad again")
    @pytest.mark.positive
    def test_ad_reappears_after_reload(self, driver):
        page = AdsPage(driver).open()
        page.wait_for_ad_to_appear()
        page.close_ad()
        assert page.is_ad_closed()
        page.open()
        with allure.step("Ad modal reappears on a fresh page load"):
            assert page.wait_for_ad_to_appear()

    @allure.title("Closing the ad does not break navigation back to the home page")
    @pytest.mark.positive
    def test_navigation_still_works_after_closing_ad(self, driver):
        page = AdsPage(driver).open()
        page.wait_for_ad_to_appear()
        page.close_ad()
        driver.get("https://practice-automation.com/")
        with allure.step("Home page loads correctly"):
            assert "practice-automation.com" in driver.current_url

    @allure.title("The ad modal is not present immediately on page load, before the countdown finishes")
    @pytest.mark.positive
    def test_ad_not_present_immediately(self, driver):
        page = AdsPage(driver).open()
        with allure.step("Ad text should not be visible in the very first moment"):
            # a generous-but-short wait; the real countdown is ~5s
            assert not page.is_visible(page.AD_MODAL_TEXT, timeout=1)


@allure.epic("practice-automation.com")
@allure.feature("Ads")
class TestAdsNegative:

    @allure.title("Closing the ad twice in a row does not raise an error")
    @pytest.mark.negative
    def test_double_close_is_safe(self, driver):
        page = AdsPage(driver).open()
        page.wait_for_ad_to_appear()
        page.close_ad()
        assert page.is_ad_closed()
        with allure.step("A second close attempt must not throw"):
            if page.exists(page.AD_MODAL_CLOSE):
                page.close_ad()
            assert page.is_ad_closed()

    @allure.title("The ad text is no longer queryable as visible after closing")
    @pytest.mark.negative
    def test_ad_text_not_visible_after_close(self, driver):
        page = AdsPage(driver).open()
        page.wait_for_ad_to_appear()
        page.close_ad()
        with allure.step("Ad text is invisible, i.e. it cannot be interacted with anymore"):
            assert not page.is_visible(page.AD_MODAL_TEXT, timeout=2)

    @allure.title("Ad modal does not appear on an unrelated page")
    @pytest.mark.negative
    def test_ad_does_not_appear_on_home_page(self, driver):
        page = AdsPage(driver)
        driver.get("https://practice-automation.com/")
        with allure.step("The ad-specific text is absent on the home page"):
            assert not page.is_visible(page.AD_MODAL_TEXT, timeout=3)
