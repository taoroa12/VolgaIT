import allure
import pytest

from pages.form_fields_page import FormFieldsPage


@allure.epic("practice-automation.com")
@allure.feature("Form Fields (task #5)")
class TestFormFields:

    @allure.title("The 'Automation tools' list is present and not empty")
    @pytest.mark.positive
    def test_automation_tools_list_is_read(self, driver):
        page = FormFieldsPage(driver).open()
        tools = page.get_automation_tools()
        allure.attach("\n".join(tools), name="automation_tools", attachment_type=allure.attachment_type.TEXT)
        with allure.step("At least one tool was read from the list"):
            assert tools
        with allure.step("Selenium is one of the listed tools"):
            assert "Selenium" in tools

    @allure.title("Message is filled with the 'Automation tools' list, comma-separated")
    @pytest.mark.positive
    def test_message_filled_with_automation_tools(self, driver):
        """Task item 5: read the list with Selenium, turn it into text, put it into Message."""
        page = FormFieldsPage(driver).open()

        with allure.step("Read the items of the 'Automation tools' list"):
            tools = page.get_automation_tools()
            assert tools, "The 'Automation tools' list is empty"

        with allure.step("Join the items into one comma-separated string"):
            tools_as_text = ", ".join(tools)
            allure.attach(tools_as_text, name="message_text", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Fill Name, Email and Message"):
            page.fill_name("Nikita QA").fill_email("nikita.qa@example.com").fill_message(tools_as_text)

        with allure.step("Message contains exactly the comma-separated list"):
            assert page.get_message_value() == tools_as_text

        with allure.step("Submit the form and accept the result alert if the site shows one"):
            page.submit()
            alert_text = page.accept_alert_if_present()
            if alert_text:
                allure.attach(alert_text, name="alert_text", attachment_type=allure.attachment_type.TEXT)

    @allure.title("Message keeps the order of the tools as shown on the page")
    @pytest.mark.positive
    def test_message_keeps_tools_order(self, driver):
        page = FormFieldsPage(driver).open()
        tools = page.get_automation_tools()
        page.fill_message(", ".join(tools))
        with allure.step("Splitting the Message by commas gives the same list back"):
            assert [t.strip() for t in page.get_message_value().split(",")] == tools
