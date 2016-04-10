from selenium.webdriver.common.by import By

from Model.CategoryPage import CategoryPage
from Model.Page import Page
from library.driver.SharedSteps import SharedSteps


class DownloadPage(CategoryPage):
    def __init__(self, driver):
        Page.__init__(self, driver)

    download_title_locator_chain_ipad = [(By.CLASS_NAME, 'UIAToolbar'), (By.NAME, 'Downloads')]
    download_title_locator_chain_iphone = [(By.CLASS_NAME, 'UIATabBar'), (By.NAME, 'Downloads')]

    @property
    def is_me(self):
        """
        :return: bool
        """
        return (SharedSteps.find_element_by_chain(self, self.download_title_locator_chain_ipad) is not None) or \
               (SharedSteps.find_element_by_chain(self, self.download_title_locator_chain_iphone) is not None)

    @property
    def is_empty(self):
        """
        :return: bool
        """
        return self.box_art_cells_count == 0

    def item_download_status_by_index(self, index):
        """
        :param index: int
        :return: str
        """
        index = int(index)
        item = self.box_art_cells[index]
        return item.get_attribute('value')

    def is_sorted_in_alphabetical_order(self, elements):
        sorted_elements = list(elements)
        sorted_elements.sort()
        assert elements == sorted_elements, \
            "Elements are not sorted alphabetically. Elements: {}, sorted elements: {}".format(elements, sorted_elements)
