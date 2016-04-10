from selenium.webdriver.common.by import By

from Model.Page import Page
from library.driver.AivAction import AivAction
from library.driver.SharedAction import SharedAction
from library.driver.SharedSteps import SharedSteps


class HomePage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    feature_content_row_locator = (By.NAME, 'Featured content')
    watch_while_abroad_hero_locator = (By.NAME, 'TV to Watch While Abroad')
    carousel_table_locator = (By.CLASS_NAME, 'UIACollectionView')
    buttons_in_row_sub_path = (By.CLASS_NAME, 'UIACollectionCell')
    search_icon_locator_chain = [(By.CLASS_NAME, 'UIANavigationBar'), (By.NAME, 'Search')]
    search_bar_locator = (By.CLASS_NAME, 'UIASearchBar')
    home_tab_iPad_locator = (By.ID, 'Toolbar_Browse_Button')
    download_tab_iPad_locator = (By.ID, 'Toolbar_Downloads_Button')
    library_tab_iPad_locator = (By.ID, 'Toolbar_Library_Button')

    ftue_close_button_locator = (By.ID, 'FTUE_Close_Button')
    ftue_first_button_locator = (By.ID, 'FTUE_First_Button')
    ftue_second_button_locator = (By.ID, 'FTUE_Second_Button')

    hero_carousel_locator = (By.ID, 'Carousel_HeroCarousel_Container')
    tab_bar_collection_locator = (By.ID, 'CatalogPage_TopBarNavigation_Collection')

    page_check_timeout = 15
    _carousel_rows_title_list = []
    _carousel_rows = None

    @property
    def did_load(self):
        """
        :return: bool
        """
        if (SharedSteps.aiv_is_element_exist(
                self.driver, *self.feature_content_row_locator,
                timeout=self.page_check_timeout) or SharedSteps.aiv_is_element_exist(
                self.driver, *self.watch_while_abroad_hero_locator, timeout=self.page_check_timeout)):
            return True  # Temporary fix while AIVIOS-6656 is in progress
        return False

    @property
    def is_me(self):
        """
        :return: bool
        """
        return self.did_load

    @property
    def top_bar_buttons(self):
        """
        :return: [WebElements]
        """
        tap_bar_collectionview = self.find_element(self.tab_bar_collection_locator)
        tab_bar_cells = tap_bar_collectionview.find_elements_by_ios_uiautomation('.cells()')
        # [0] is HOME, [1] is TV SHOWS, [2] is MOVIES
        return tab_bar_cells

    @property
    def top_bar_home_button(self):
        """
        :return: WebElement
        """
        return self.top_bar_buttons[0]

    @property
    def top_bar_tv_shows_button(self):
        """
        :return: WebElement
        """
        return self.top_bar_buttons[1]

    @property
    def top_bar_movies_button(self):
        """
        :return: WebElement
        """
        return self.top_bar_buttons[2]

    @property
    def hero_carousel(self):
        """
        :return: WebElement
        """
        return self.find_element(self.hero_carousel_locator)

    @property
    def feature_content_row(self):
        """
        :return: WebElement
        """
        return self.driver.find_element(*self.feature_content_row_locator)

    @property
    def carousel_rows(self):
        """
        :return: list[WebElement]
        """
        if self._carousel_rows is None:
            self._carousel_rows = self.find_element(self.carousel_table_locator).find_elements_by_ios_uiautomation('.cells()')
        return self._carousel_rows

    @property
    def carousel_rows_title_list(self):
        """
        :return: list[str]
        """
        if len(self._carousel_rows_title_list) == 0:
            for row in self.carousel_rows:
                self._carousel_rows_title_list.append(row.get_attribute('name'))
        return self._carousel_rows_title_list

    @property
    def browse_popover_menu(self):
        return self.driver.find_element(By.CLASS_NAME, 'UIAPopover')

    @property
    def search_bar(self):
        return self.driver.find_element(*self.search_bar_locator)

    @property
    def search_icon(self):
        return SharedSteps.find_element_by_chain(self, self.search_icon_locator_chain)

    @property
    def tab_bar_items(self):
        return self.find_element((By.CLASS_NAME, 'UIATabBar')).find_elements_by_ios_uiautomation('.buttons()')

    def get_link_text_from_row(self, title):
        """
        :param title: str
        :return: WebElement
        """
        for row in self.carousel_rows:
            if row.text == title:
                return row.find_element(*self.buttons_in_row_sub_path)
        return None

    def get_all_buttons_from_row(self, title):
        """
        :param title: str
        :return: list{WebElement}
        """
        for row in self.carousel_rows:
            if (row.text != '' and row.text == title) or (row.get_attribute('name') == title):
                return row.find_elements(*self.buttons_in_row_sub_path)

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
        if self.is_element_exist(self.ftue_first_button_locator, timeout=5):
            self.find_element(self.ftue_first_button_locator).click()

    def by_pass_push_notifcation(self):
        if self.is_element_exist(self.ftue_second_button_locator, timeout=5):
            self.find_element(self.ftue_second_button_locator).click()

    def nav_to_download_tab(self):
        if self.is_element_exist(self.download_tab_iPad_locator):
            self.find_element(self.download_tab_iPad_locator).click()
        else:
            self.tab_bar_items[3].click()

    def nav_to_yvl_tab(self):
        if self.is_element_exist(self.library_tab_iPad_locator):
            self.find_element(self.library_tab_iPad_locator).click()
        else:
            self.tab_bar_items[2].click()

    def nav_to_home_tab(self):
        if self.is_element_exist(self.home_tab_iPad_locator):
            self.click_button_by_locator(self.home_tab_iPad_locator)
        else:
            self.tab_bar_items[0].click()


