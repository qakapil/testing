from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from Model.Page import Page
from library.driver.SharedSteps import SharedSteps


class AccountRegistrationPage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    create_account_label_locator = (By.NAME, 'Create Account')
    web_view_element_locator = (By.CLASS_NAME, 'UIAWebView')
    navigation_bar_locator = (By.NAME, 'Amazon.com Registration')

    @property
    def did_load(self):
        """
        :return: bool
        """
        if SharedSteps.aiv_is_element_exist(self.driver, *self.web_view_element_locator):
            web_view = self.web_view
            if web_view is not None:
                try:
                    SharedSteps.aiv_is_element_exist(web_view, *self.create_account_label_locator)
                    return True
                except NoSuchElementException:
                    return False
        return False

    @property
    def web_view(self):
        """
        :return: WebElement or None
        """
        return SharedSteps.page_web_element_getter(self.driver, self.web_view_element_locator)

    @property
    def navigation_bar(self):
        """
        :return: WebElement or None
        """
        return SharedSteps.page_web_element_getter(self.web_view, self.navigation_bar_locator)



