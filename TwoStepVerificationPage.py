from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from Model.Page import Page
from library.driver.SharedSteps import SharedSteps


class TwoStepVerificationPage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    two_step_verification_title_locator = (By.NAME, 'Two-Step Verification')
    web_view_element_locator = (By.CLASS_NAME, 'UIAWebView')

    @property
    def did_load(self):
        """
        :return: bool
        """
        if SharedSteps.aiv_is_element_exist(self.driver, *self.web_view_element_locator):
            web_view = self.driver.find_element(*self.web_view_element_locator)
            if web_view is not None:
                try:
                    web_view.find_element(*self.two_step_verification_title_locator)
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



