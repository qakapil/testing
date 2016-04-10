import time

from selenium.webdriver.common.by import By

from Model.CategoryPage import CategoryPage
from library import Constant
from library.driver.SharedAction import SharedAction
from library.driver.SharedSteps import SharedSteps
from library.config_manager import ConfigManager

class RefinePage(CategoryPage):
    """A base class for Watchlist page, Library page, and Downloads page."""
    def __init__(self, driver):
        CategoryPage.__init__(self, driver)

    buttons_locator = (By.CLASS_NAME, 'UIAButton')
    refine_bar_locator = (By.NAME, 'Refine')
    # TODO: the locator of empty library message is missing, need to contact dev team to add accessibility attribute onto it.
    body_message_locator = (By.NAME, 'body')
    refine_options_locator_chain = [(By.CLASS_NAME, 'UIAElement'), (By.CLASS_NAME, 'UIAButton')]

    @property
    def is_empty(self):
        """
        :return: bool
        """
        return self.box_art_cells_count == 0

    @property
    def refine_button(self):
        buttons = self.find_elements(self.buttons_locator)
        if SharedAction.is_button_found(buttons, self.refine_bar_locator[1]):
            for button in buttons:
                if button.text == self.refine_bar_locator[1]:
                    return button
        else:
            return None

    @property
    def did_load(self):
        """
        :return: bool
        """
        return SharedSteps.aiv_is_element_exist(self.driver, *self.refine_bar_locator)

    @property
    def is_me(self):
        """
        :return: bool
        """
        return SharedSteps.aiv_is_element_exist(self.driver, *self.refine_bar_locator, timeout=2)

    @property
    def sort_by(self):
        """
        :return: str
        """
        self.wait_sort_by_text_appears('Showing')
        return self.refine_button.get_attribute('value')

    @property
    def body_message(self):
        """
        :return: str
        """
        el = self.find_element(self.body_message_locator)
        if el is not None:
            return el.text
        else:
            return ''

    def wait_sort_by_text_appears(self, text):

        timeout = time.time() + Constant.driver_wait_timeout
        while True:
            if self.refine_button.get_attribute('value').find(text) == -1:
                SharedSteps.aiv_driver_wait(self.driver, *self.refine_bar_locator)
            else:
                break
            time.sleep(1)
            if time.time() > timeout:
                break

    def select_refine_option(self, option_name):
        """
        :param option_name: str
        """
        self.refine_button.click()
        refine_options = SharedSteps.find_element_by_chain(self, self.refine_options_locator_chain, True)
        for button in refine_options:
            if button.text == option_name:
                button.click()
                break
