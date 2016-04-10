import re

from selenium.webdriver.common.by import By

from Model.Page import Page
from library.driver.SharedSteps import SharedSteps
from library.utilities.extensions import AIVElement
from library.driver.SharedAction import SharedAction


class SearchResultPage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    search_results_list_locator = (By.CLASS_NAME, 'UIACollectionView')
    search_result_item_locator = (By.CLASS_NAME, 'UIACollectionCell')
    search_result_items_locator_chain = [search_results_list_locator, search_result_item_locator]
    header_locator = (By.ID, 'Search_Header_Label')
    header_results_summary_label = (By.ID, 'Search_ResultsSummary_Label')

    refine_locator = (By.ID, 'Search_Refine_Button')
    refine_movie_locator = (By.ID, 'Search_MovieRefine_Button')
    refine_tv_locator = (By.ID, 'Search_TVRefine_Button')
    refine_prime_locator = (By.ID, 'Search_PrimeRefine_Button')
    refine_free_episode_locator = (By.ID, 'Search_FreeEpisodeRefine_Button')
    refine_xray_locator = (By.ID, 'Search_XRayRefine_Button')
    refine_done_locator = (By.ID, 'Search_RefineDone_Button')

    search_results_movie_locator = (By.ID, 'Search_ResultMovie_Button')
    search_results_tv_locator = (By.ID, 'Search_ResultTV_Button')
    search_results_xray_locator = (By.ID, 'Search_Result_XRay_Image')

    @property
    def did_load(self):
        """
        :return: bool
        """
        return SharedSteps.aiv_driver_wait_visible_retry(self.driver, self.header_results_summary_label)

    @property
    def is_me(self):
        """
        :return: bool
        """
        return self.is_element_exist(self.header_locator, timeout=2)

    @property
    def search_result_item_list(self):
        """
        :return list[WebElement] or None
        """
        if self.is_element_exist(self.search_results_list_locator):
            return self.find_element_by_chain(self.search_result_items_locator_chain, return_list=True)

    @property
    def search_result_movie_list(self):
        """
        :return list[WebElement] or None
        """
        items = self.search_result_item_list
        movies = [item for item in items if item.get_attribute('name') == self.search_results_movie_locator[1]]
        return movies


    @property
    def search_result_tv_list(self):
        """
        :return list[WebElement] or None
        """
        items = self.search_result_item_list
        tvs = [item for item in items if item.get_attribute('name') == self.search_results_tv_locator[1]]
        return tvs


    @property
    def search_results_header_count_text(self):
        """
        :return: str
        """
        return self.find_element(self.header_locator).get_attribute('value')

    @property
    def search_results_count(self):
        """
        :return: int
        """
        search_summary = AIVElement(self.find_element(self.header_locator)).value
        match = re.search('\d+', search_summary)
        if match:
            count = match.group()
            return int(count)
        else:
            return 0

    @property
    def search_refine_button(self):
        """
        :return: WebElement or None
        """
        if self.is_element_exist(self.refine_locator):
            return self.find_element(self.refine_locator)
        return None

    @property
    def search_refine_prime_button(self):
        """
        :return WebElement or None
        """
        if self.is_element_exist(self.refine_prime_locator):
            return self.find_element(self.refine_prime_locator)
        return None

    @property
    def search_refine_xray_button(self):
        """
        :return WebElement or None
        """
        if self.is_element_exist(self.refine_xray_locator):
            return self.find_element(self.refine_xray_locator)
        return None

    @property
    def refine_done(self):
        """
        :return: WebElement or None
        """
        if self.is_element_exist(self.refine_done_locator):
            return self.find_element(self.refine_done_locator)
        return None

    def apply_free_episode_filter(self):
        self.__apply_filter_by(self.refine_free_episode_locator)

    def apply_movie_filter(self):
        self.__unselect_option_if_selected(self.refine_tv_locator)
        self.__select_option_if_unselected(self.refine_movie_locator)

    def apply_tv_filter(self):
        self.__unselect_option_if_selected(self.refine_movie_locator)
        self.__select_option_if_unselected(self.refine_tv_locator)

    def apply_xray_filter(self):
        self.__apply_filter_by(self.refine_xray_locator)

    def __apply_filter_by(self, button_locator):
        # Be careful of using this method, sometimes click the option means unselected it.
        self.search_refine_button.click()
        self.__find_button_and_apply(button_locator)

    def __find_button_and_apply(self, locator):
        if self.is_element_exist(locator):
            self.find_element(locator).click()
            if self.refine_done is not None:
                self.refine_done.click()

    def __quit_refine(self):
        if self.refine_done is not None:
            self.refine_done.click()
        else:
            SharedAction.click_element_behind_overlay(self.driver,self.search_refine_button)

    def __unselect_option_if_selected(self, locator):
        """
        :param locator: filter option locator
        """
        if self.find_element(locator) is None:
            self.search_refine_button.click()
        if AIVElement(self.find_element(locator)).value == 1:
            self.__find_button_and_apply(locator)

    def __select_option_if_unselected(self, locator):
        """
        :param locator: filter option locator
        """
        if self.find_element(locator) is None:
            self.search_refine_button.click()
        if AIVElement(self.find_element(locator)).value == '':
            self.__find_button_and_apply(locator)
        else:
            self.__quit_refine()

    def wait_for_search_page_to_reload(self, before_count):
        SharedSteps.aiv_driver_wait_text_to_change(self.driver, self.header_locator, before_count)

    def result_has_movies(self):
        return True if len(self.find_elements(self.search_results_movie_locator)) > 0 else False

    def result_has_tv_shows(self):
        return True if len(self.find_elements(self.search_results_tv_locator)) > 0 else False
