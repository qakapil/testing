import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from Model.Page import Page
from library import Constant
from library.driver.SharedSteps import SharedSteps
from library.config_manager import ConfigManager
from library.utilities.extensions import AIVElement


def is_text_empty(text):
    return text == ''


class CategoryPage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    category_unique_locator = (By.NAME, 'AIVBrowsePageViewController')
    collections_locator = (By.CLASS_NAME, 'UIACollectionView')
    box_art_sub_locator = (By.CLASS_NAME, 'UIACollectionCell')

    @property
    def is_me(self):
        """
        :return: bool
        """
        return SharedSteps.aiv_is_element_exist(self.driver, *self.category_unique_locator)

    def get_category_element(self, category):
        """
        :return: WebElement or None
        """
        try:
            return self.driver.find_element_by_name(category)
        except WebDriverException:
            return None

    @property
    def box_art_cells(self):
        """
        :return: list[WebElement]
        """
        SharedSteps.aiv_is_element_list_exist(self.driver, self.collections_locator)
        cell_list = self.driver.find_elements(*self.collections_locator)[-1].find_elements(*self.box_art_sub_locator)

        # TODO: not very efficient as it iterate thru the entire list. Maybe check the first item is empty then remove?
        #is_not_empty_title = lambda cell: cell.text != ''
        #return filter(is_not_empty_title, cell_list)

        if cell_list[0].text == '':
            cell_list.pop(0)
        return cell_list

    def fetch_cell_by_title(self, title):
        """
        :param title: str
        :return: WebElement or None
        """
        for cell in self.box_art_cells:
            if AIVElement(cell).aiv_text.lower() == title.lower():
                return cell

        return None

    @property
    def box_art_cells_count(self):
        """
        :return: int
        """
        return len(self.box_art_cells)

    def wait_specific_box_art_cell(self, index):
        timeout = time.time() + Constant.driver_wait_timeout
        while True:
            if self.box_art_cells[index].text != '':
                SharedSteps.aiv_driver_wait(self.driver, By.NAME, self.box_art_cells[index].text)
                break
            time.sleep(1)
            if time.time() > timeout:
                break
