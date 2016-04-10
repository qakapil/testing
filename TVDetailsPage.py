import logging
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from Model.DetailsBasePage import DetailsBasePage
from library.driver.AivAction import AivAction
from library.driver.SharedAction import SharedAction
from library.driver.SharedSteps import SharedSteps
from random import randint
from library.utilities.extensions import AIVElement
from library.logger import Logger


class TVDetailsPage(DetailsBasePage):
    def __init__(self, driver):
        DetailsBasePage.__init__(self, driver)

    tv_details_container_locator = (By.CLASS_NAME, 'UIATableView')
    tv_episode_container_locator = (By.CLASS_NAME, 'UIATableCell')
    episode_play_button_locator = (By.NAME, 'Play')
    episode_download_button_locator = (By.ID, 'TVDetailPage_Download')
    episode_delete_download_button_locator = (By.NAME, 'TVDetailPage_Delete_Download')
    episode_node_cell_locator = (By.ID, 'DetailsPage_EpisodeNode_Cell')
    play_options_popover_locator = (By.CLASS_NAME, 'UIAPopover')
    start_over_button_locator = (By.NAME, 'Start Over')
    promotional_button_in_episode_node_locator = (By.CLASS_NAME, 'UIAButton')
    free_with_ads_label_locator = (By.ID, 'AVOD_FreeWithAds_Label')
    notification_ok_button_name = (By.NAME, 'OK')
    notification_delete_button_name = (By.NAME, 'Delete')

    @property
    def is_me(self):
        if super(TVDetailsPage, self).is_me:
            return self.is_element_exist(self.tv_details_container_locator, timeout=5)

    @property
    def did_load(self):
        if super(TVDetailsPage, self).did_load:
            return self.is_element_exist(self.tv_details_container_locator, timeout=10)

    @property
    def episode_nodes_count(self):
        """
        :return: int
        """
        return len(self.episode_nodes)

    @property
    def play_options_popover(self):
        """
        :return: WebElement or None
        """
        return self.find_element(self.play_options_popover_locator)

    @property
    def episode_nodes(self):
        """
        :return: list[WebElement] or None
        """
        episode_nodes_container = self.find_element(self.tv_details_container_locator)
        cells = episode_nodes_container.find_elements(*self.episode_node_cell_locator)
        episode_cells = [episode_cell for episode_cell in cells if episode_cell.get_attribute('value') == '']
        return episode_cells

    # downloaded episodes could not be caught by episode_nodes
    @property
    def downloaded_nodes(self):
        """
        :return: list[WebElement] or None
        """
        episode_nodes_container = self.find_element(self.tv_details_container_locator)
        cells = episode_nodes_container.find_elements(*self.tv_episode_container_locator)
        episode_cells = [episode_cell for episode_cell in cells
                         if len(episode_cell.find_elements(*self.episode_delete_download_button_locator))]
        return episode_cells

    @property
    def tv_season_title_element(self):
        """
        return: WebElement or None
        """
        tv_details_container = self.find_element(self.tv_details_container_locator)
        cell_nodes = tv_details_container.find_elements_by_ios_uiautomation('.cells()')  # Episode details

        return cell_nodes[0]

    @property
    def get_random_episode_index(self):
        """
        :return: Index of a random episode
        :type int
        """
        random_index = randint(0, self.episode_nodes_count - 1)
        return random_index

    def play_episode_by_index(self, index):
        """
        :param index: int
        """
        ep = self.episode_nodes[index]
        AivAction(self.driver).scroll_to_element(ep)
        play_button = ep.find_element(*self.episode_play_button_locator)

        play_button.click()

        if self.play_options_popover is not None or self.is_element_exist(self.start_over_button_locator):
            SharedAction.click_first_visible_button(self.find_elements(self.start_over_button_locator))

    def is_episode_node_expanded(self, episode_node):
        """

        :type episode_node: WebElement
        """
        # If the last static text is visible, it is expanded.
        return AIVElement(episode_node.find_elements(By.CLASS_NAME, 'UIAStaticText')[-1]).aiv_is_displayed()

    def is_episode_node_expandable(self, episode_node):
        """
        :type episode_node: WebElement
        """
        self.move_episode_node_in_screen(episode_node)

        # Collapse the episode node if it is expanded
        if self.is_episode_node_expanded(episode_node):
            episode_node.click()

        height_collapse = episode_node.size['height']

        # Expand the episode node
        episode_node.click()

        height_expand = episode_node.size['height']

        # Verify the episode node has been expanded
        assert self.is_episode_node_expanded(episode_node) is True

        Logger.debug('height_expand is {}; height_collapse is {}'.format(height_expand, height_collapse))

        assert height_expand > height_collapse, \
            "The episode node has not expanded, height_expand is {}, height_collapse is {}".\
                format(height_expand, height_collapse)

        # Collapse the episode node
        episode_node.click()

        height_collapse = episode_node.size['height']

        # Verify the episode node has been collapsed
        assert self.is_episode_node_expanded(episode_node) is False
        Logger.debug('height_expand is {}; height_collapse is {}'.format(height_expand, height_collapse))
        assert height_expand > height_collapse, \
            "The episode node has not collapsed, height_expand is {}, height_collapse is {}".\
                format(height_expand, height_collapse)

    def tap_promotional_button_under_episode_index(self, index):
        """
        :param index: Random episode index
        :type int
        """
        episode_obj = self.episode_nodes[index]
        AivAction(self.driver).scroll_to_element(episode_obj)
        episode_obj.click()
        episode_node_promotional_button = episode_obj.find_element(*self.promotional_button_in_episode_node_locator)
        episode_node_promotional_button.click()

    def is_episode_free_by_index(self, index=0):
        """
        :param index: int
        :return: bool
        """
        episode_node = self.episode_nodes[index]
        return AIVElement(episode_node).contains_element(self.free_with_ads_label_locator)

    def move_episode_node_in_screen(self, episode_node):
        if not episode_node.is_displayed():
            AivAction(self.driver).scroll_to_element(episode_node)
        else:
            AivAction(self.driver).move_element_by_y(episode_node, -episode_node.size['height'])

    def start_download_by_index(self, index):
        """
        :param index: int
        """
        download_button = self.episode_nodes[index].find_element(*self.episode_download_button_locator)
        AivAction(self.driver).scroll_to_element(download_button)
        download_button.click()

        SharedAction.click_button_by_locator(self.driver,self.notification_ok_button_name)

    def delete_download_by_index(self, index):
        """
        :param index: int
        """
        delete_button = self.downloaded_nodes[index].find_element(*self.episode_delete_download_button_locator)
        AivAction(self.driver).scroll_to_element(delete_button)
        delete_button.click()

        SharedAction.click_button_by_locator(self.driver,self.notification_delete_button_name)

    def play_downloaded_by_index(self,index):
        """
        :param index: int
        """
        downloaded = self.downloaded_nodes[index]
        play_button = downloaded.find_element(*self.episode_play_button_locator)
        play_button.click()
        if self.play_options_popover is not None or self.is_element_exist(self.start_over_button_locator):
            SharedAction.click_first_visible_button(self.find_elements(self.start_over_button_locator))

        SharedAction.click_button_by_locator(self.driver,self.notification_ok_button_name)

