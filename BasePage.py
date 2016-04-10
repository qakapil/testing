from selenium.webdriver.common.by import By

from Model.Page import Page
from library.driver.SharedSteps import SharedSteps


class BasePage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    settings_button_locator = (By.NAME, 'Settings')
    my_account_cell_locator = (By.NAME, 'My Account')
    sign_out_button_locator = (By.NAME, 'Sign Out')

    def logout(self):
        _driver = self.driver
        """
        :type _driver webdriver.Remote
        """
        for element in _driver.find_elements(*self.settings_button_locator):
            if element.tag_name == 'UIAButton' and element.is_displayed():
                element.click()
                for el in self.find_elements(self.my_account_cell_locator):
                    if el.tag_name == 'UIATableCell':
                        el.click()
                        self.driver.find_element(*self.sign_out_button_locator).click()
                        break
        # Sometimes when current account has download item, it will ask user to confirm you still want to logout.
        self.click_button('Sign Out')

    @property
    def settings_pop_over(self):
        """
        :return: appium.webdriver.WebElement
        """
        return self.driver.find_element(By.CLASS_NAME, 'UIAPopover')

    @property
    def did_load(self):
        """
        :return: bool
        """
        return SharedSteps.aiv_is_element_exist(self.driver, *self.settings_button_locator)

    @property
    def is_me(self):
        """
        :return: bool
        """
        return SharedSteps.aiv_is_element_exist(self.driver, *self.settings_button_locator, timeout=5)