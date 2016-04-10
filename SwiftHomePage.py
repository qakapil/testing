from selenium.webdriver.common.by import By

from Model.Page import Page
from library.driver.SharedSteps import SharedSteps


class SwiftHomePage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    feature_content_row_locator = (By.NAME, 'Featured content')
    carousel_table_locator_chain = [(By.NAME, 'AIVLandingPageViewController'), (By.CLASS_NAME, 'UIACollectionView')]
    carousel_rows_text_locator_chain = carousel_table_locator_chain + [(By.CLASS_NAME, 'UIAStaticText')]
    buttons_in_row_sub_path = (By.CLASS_NAME, 'UIACollectionCell')
    row_collection_sub_path = (By.CLASS_NAME, 'UIACollectionView')
    search_box_locator = (By.CLASS_NAME, 'UIASearchBar')
    get_started_button_locator = (By.NAME, 'Get Started')
    page_check_timeout = 15
    _carousel_rows_title_list = []
    _carousel_rows = None
    isRefreshed = False

    @property
    def did_load(self):
        """
        :return: bool
        """
        return SharedSteps.aiv_is_element_exist(
            self.driver, *self.feature_content_row_locator, timeout=self.page_check_timeout)

    @property
    def is_me(self):
        """
        :return: bool
        """
        return SharedSteps.aiv_is_element_exist(
            self.driver, *self.feature_content_row_locator, timeout=5)

    @property
    def feature_content_row(self):
        """
        :return: WebElement
        """
        return self.driver.find_element(*self.feature_content_row_locator)

    @property
    def carousel_collection(self):
        """
        :return: list[WebElement]
        """
        return SharedSteps.find_element_by_chain(self, self.carousel_table_locator_chain)

    @property
    def title_static_text_element_list(self):

        # this list mixes the carousel title and see more
        """
        :return: list[WebElement]
        """
        return SharedSteps.find_element_by_chain(self, self.carousel_rows_text_locator_chain, True)

    @property
    def carousel_rows_title_list(self):
        """
        :return: list[str]
        """
        if len(self._carousel_rows_title_list) == 0 or (not self.isRefreshed):
            self._carousel_rows_title_list = []
            for row in self.title_static_text_element_list:
                if not row.text.find('See more ') == 0:
                    self._carousel_rows_title_list.append(row.text)
        return self._carousel_rows_title_list

    @property
    def browse_popover_menu(self):
        return self.driver.find_element(By.CLASS_NAME, 'UIAPopover')

    @property
    def search_box(self):
        return self.driver.find_element(*self.search_box_locator)

    def get_link_text_from_row(self, title):
        """
        :param title: str
        :return: WebElement
        """
        for index, row in enumerate(self.title_static_text_element_list):
            if row.text == title:
                # return the next text element after title
                return self.title_static_text_element_list[index + 1]
        return None

    def get_all_buttons_from_row(self, index):
        """
        :param title: str
        :param index: int
        :return: list{WebElement}
        """
        return self.carousel_collection.find_elements(*self.row_collection_sub_path)[int(index)]. \
            find_elements(*self.buttons_in_row_sub_path)

    def get_index_by_row_name(self, name, prefix_match_only=False):
        """
        :param name: str
        :param prefix_match_only: bool
        :return: int
        """
        for index, row in enumerate(self.carousel_rows_title_list):
            if prefix_match_only:
                if row.find(name) == 0:
                    return index
            else:
                if row == name:
                    return index
        return -1

    def by_pass_get_started_prompt(self):
        if SharedSteps.aiv_is_element_exist(self.driver, *self.get_started_button_locator):
            self.find_element(self.get_started_button_locator).click()
