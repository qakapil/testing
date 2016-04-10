from selenium.webdriver.common.by import By

from Model.CategoryPage import CategoryPage


class LibraryPage(CategoryPage):
    def __init__(self, driver):
        CategoryPage.__init__(self, driver)

    library_segmentcontrol_locator = (By.ID, 'Library_MoviesTV_SegmentControl')
    library_refine_locator = (By.ID, 'Library_Refine_Button')
    refine_title_locator = (By.ID, 'Refine_Title_Button')
    refine_recently_added_locator = (By.ID, 'Refine_RecentlyAdded_Button')
    library_title_collection_locator = (By.CLASS_NAME, 'UIACollectionView')

    text_to_locator \
        = dict([('Refine', library_refine_locator),
                ('Title', refine_title_locator),
                ('SegmentControl', library_segmentcontrol_locator)])

    tab_name_to_index \
        = dict([('Movies', 0),
                ('TV', 1)])

    @property
    def did_load(self):
        """
        :return: bool
        """
        return self.is_element_exist(self.library_segmentcontrol_locator)

    @property
    def is_me(self):
        """
        :return: bool
        """
        return self.is_element_exist(self.library_segmentcontrol_locator)

    @property
    def refine_button(self):
        return self.find_element(self.library_refine_locator)

    def get_tab_by_name(self, name):
        segment_control = self.find_element(self.library_segmentcontrol_locator)
        tabs = segment_control.find_elements_by_ios_uiautomation('.buttons()')
        return tabs[self.tab_name_to_index[name]]

    def refine_titles_by_option(self, option):
        self.refine_button.click()
        if option == 'Title':
            button = self.find_element(self.refine_title_locator)
        else:
            button = self.find_element(self.refine_recently_added_locator)

        button.click()

    def click_download_item(self, index):
        """
        :param index: int
        """
        index = int(index)
        self.wait_specific_box_art_cell(index)
        self.box_art_cells[index].click()