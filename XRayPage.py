from Model.CategoryPage import *


class XrayPage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    xray_inscene_collection_view_locator = (By.ID, "Xray_InScene_CollectionView");
    xray_tabs_view_locator = (By.ID, "Xray_Tabs_View")

    tab_name_to_locator \
        = dict([('In Scene', xray_inscene_collection_view_locator)])

    @property
    def did_load(self):
        """
        :return: bool
        """
        return SharedSteps.aiv_is_element_exist(
            self.driver, *self.xray_tabs_view_locator, timeout=self.page_check_timeout)

    @property
    def is_me(self):
        """
        :return: bool
        """
        return SharedSteps.aiv_is_element_exist(
            self.driver, *self.xray_tabs_view_locator)

    def is_current_tab(self, tab_name):
        locator = self.tab_name_to_locator[tab_name]
        return self.is_element_exist(locator)
