from selenium.webdriver.common.by import By

from Model.Page import Page


class SettingsPage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    settings_label_locator = (By.NAME, 'Settings')
    about_cell_locator = (By.ID, "Settings_About_Cell")
    my_account_cell_locator = (By.ID, "Settings_MyAccount_Cell")
    manage_data_usage_cell_locator = (By.ID, "Settings_ManageDataUsage_Cell")
    download_quality_cell_locator = (By.ID, "Settings_DownloadQuality_Cell")
    download_quality_text_cell_locator = (By.ID, "Settings_DownloadQuality_Text")
    autoplay_cell_locator = (By.ID, "Settings_AutoPlay_Cell")
    notifications_cell_locator = (By.ID, "Settings_Notifications_Cell")
    parental_controls_cell_locator = (By.ID, "Settings_ParentalControls_Cell")
    contact_us_cell_locator = (By.ID, "Settings_ContactUs_Cell")
    legal_information_cell_locator = (By.ID, "Settings_LegalInformation_Cell")
    about_heading_locator = (By.ID, "About_Heading_Element")
    myaccount_signout_locator = (By.ID, "MyAccount_SignOut_Button")
    managedatausage_wifionly_locator = (By.ID, "StreamingQuality_WifiOnly_Cell")
    downloadquality_low_locator = (By.ID, "DownloadQuality_Low_Cell")
    autoplay_allow_locator = (By.ID, "AutoPlay_Allow_Cell")
    notifications_all_locator = (By.ID, "Notifications_Allow_Cell")
    parentalcontrols_touchidenabled_locator = (By.ID, "ParentalControls_TouchIDEnabled_Cell")
    contactus_prividefeedback_locator = (By.ID, "ContactUs_ProvideFeedback_Cell")
    legalinformation_privacypolicy_locator = (By.ID, "LegalInformation_PrivacyPolicy_Cell")

    name_to_cell_locator \
        = dict([('About', about_cell_locator),
                ('My Account', my_account_cell_locator),
                ('Manage Data Usage', manage_data_usage_cell_locator),
                ('Download Settings', download_quality_cell_locator),
                ('Auto Play', autoplay_cell_locator),
                ('Notifications', notifications_cell_locator),
                ('Parental Controls', parental_controls_cell_locator),
                ('Contact Us', contact_us_cell_locator),
                ('Legal Information', legal_information_cell_locator)])

    sub_page_to_locator \
        = dict([('About', about_heading_locator),
                ('My Account', myaccount_signout_locator),
                ('Manage Data Usage', managedatausage_wifionly_locator),
                ('Download Settings', downloadquality_low_locator),
                ('Auto Play', autoplay_allow_locator),
                ('Notifications', notifications_all_locator),
                ('Parental Controls', parentalcontrols_touchidenabled_locator),
                ('Contact Us', contactus_prividefeedback_locator),
                ('Legal Information', legalinformation_privacypolicy_locator)])

    quality_level_to_accessibility_id \
        = dict([('Good', 'DownloadQuality_Low_Cell'),
                ('Better', 'DownloadQuality_Medium_Cell'),
                ('Best', 'DownloadQuality_High_Cell')])

    @property
    def did_load(self):
        return self.is_element_exist(self.about_cell_locator)

    @property
    def is_me(self):
        return self.is_element_exist(self.about_cell_locator)

    @property
    def download_quality_level(self):
        download_quality_level_element = self.find_element(self.download_quality_text_cell_locator)
        return download_quality_level_element.get_attribute('value')

    def is_current_settings_sub_page(self, sub_page_name):
        locator = self.sub_page_to_locator[sub_page_name]
        return self.is_element_exist(locator)

    def is_current_element_checked(self, cell):
        value = cell.get_attribute('value')
        return value == 1

    def get_download_quality_element(self, accessibility_id):
        return self.get_element_by_id(accessibility_id)

    def get_option_by_name(self, name):
        option_locator = self.name_to_cell_locator[name]
        return self.find_element(option_locator)

    def scroll_to_settings_option(self, option):
        self.driver.aiv_action.scroll_to_element(option)
