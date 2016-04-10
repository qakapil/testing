from abc import abstractproperty

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from library import Constant
from library.driver.SharedAction import SharedAction
from library.driver.SharedSteps import SharedSteps


class Page(object):

    def __init__(self, driver):
        self.driver = driver

    @abstractproperty
    def is_me(self):
        return

    @abstractproperty
    def did_load(self):
        return

    def find_element(self, loc):
        """
        :param loc: (By, Name)
        :return: WebElement
        """
        try:
            return self.driver.find_element(*loc)
        except NoSuchElementException:
            return None

    def find_elements(self, loc):
        """
        :param loc: (By, Name)
        :return: list{Element}
        """
        try:
            return self.driver.find_elements(*loc)
        except NoSuchElementException:
            return None

    def accept_alert(self):
        self.driver.switch_to.alert.accept()

    def is_element_exist(self, locator, timeout=Constant.page_check_timeout):
        """
        :param locator: (By, Name)
        :param timeout: int
        :return: bool
        """
        return SharedSteps.aiv_is_element_exist(self.driver, *locator, timeout=timeout)

    def click_button(self, button_name):
        """
        :param button_name: str
        """
        assert isinstance(button_name, str)
        elements = self.find_elements([By.NAME, button_name])
        SharedAction.click_first_visible_button(elements)

    def click_button_by_locator(self, locator):
        """
        :param locator: [by, name]
        """
        SharedAction.click_button_by_locator(self.driver, locator)

    def find_element_by_chain(self, locator_chain, return_list=False):
        """
        :param locator_chain: [(By, Name), (By, Name)]
        :param return_list: bool
        :return: bool
        """
        return SharedSteps.find_element_by_chain(self, locator_chain, return_list)

    def get_element_by_id(self, accessibility_id):
        locator = (By.ID, accessibility_id)
        return self.find_element(locator)