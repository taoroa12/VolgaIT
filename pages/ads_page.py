"""Page object for https://practice-automation.com/ads/

The page copy says "An ad will appear in 5...4...3...2...1", i.e. the ad
modal ("Hi / I am an ad.") shows itself automatically a few seconds after
page load, with no user action needed. Like the other popups on this site
it's a Popup Maker popup, closed via the same
"pum-close popmake-close" button (see modals_page.py for the captured
markup), scoped to the currently active popup.
"""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

AD_APPEAR_TIMEOUT = 12  # the page counts down from 5, give it margin


class AdsPage(BasePage):
    URL = "https://practice-automation.com/ads/"

    AD_MODAL_TEXT = (By.XPATH, "//*[contains(text(), 'I am an ad')]")
    AD_MODAL_CLOSE = (By.CSS_SELECTOR, ".pum-active .pum-close.popmake-close")

    def wait_for_ad_to_appear(self) -> bool:
        return self.is_visible(self.AD_MODAL_TEXT, timeout=AD_APPEAR_TIMEOUT)

    def close_ad(self):
        self.click(self.AD_MODAL_CLOSE)
        # Popup Maker fades the popup out rather than removing it instantly,
        # so wait here instead of leaving the race to whoever calls close_ad().
        self.is_invisible(self.AD_MODAL_TEXT, timeout=self.timeout)
        return self

    def is_ad_closed(self) -> bool:
        return self.is_invisible(self.AD_MODAL_TEXT, timeout=5)
