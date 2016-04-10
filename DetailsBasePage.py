import re

from Model.CategoryPage import *
from library.driver.SharedSteps import SharedSteps
from library.logger import Logger
from library.utilities.extensions import AIVElement


class DetailsBasePage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    detail_similar_titles_locator = (By.ID, 'DetailsPage_SimilarTitles_TableCell')
    detail_title_locator = (By.ID, 'DetailsPage_Title_StaticText')
    synopsis_label_locator = (By.ID, 'DetailsPage_Synopsis_Container')
    cast_collection_locator = (By.ID, 'IMDb_Cast_Collection')
    director_button_locator = (By.ID, 'IMDb_Director_Cell')
    see_full_cast_button_locator = (By.ID , 'IMDb_SeeFullCast_Button')
    see_more_at_imdb_button_locator = (By.ID, 'IMDb_SeeMoreAtIMDb_Button')
    imdb_compact_rating_locator = (By.ID, 'IMDb_CompactRating_Element')
    imdb_rating_locator = (By.ID, 'IMDb_Rating_Element')
    imdb_details_locator = (By.ID, 'IMDb_Details_Element')
    ui_alert_locator = (By.CLASS_NAME, 'UIAAlert')
    how_do_I_watch_popup_text_locator_chain = [ui_alert_locator, (By.CLASS_NAME, 'UIAStaticText')]
    pin_secure_text_field_locator_chain = [ui_alert_locator, (By.CLASS_NAME, 'UIASecureTextField')]
    thirdparty_how_do_I_watch_this_locator = (By.ID, 'DetailsPage_3PHowDoIWatchThis_Button')
    how_do_I_watch_this_locator = (By.ID, 'DetailsPage_HowDoIWatchThis_Button')
    watch_with_prime_locator = (By.ID, 'DetailsPage_WatchWithPrime_Button')
    thirdparty_greystripe_locator = (By.ID, 'DetailsPage_ThirdPartyGreyStripe_StaticText')
    prime_upgrade_grey_stripe_locator = (By.ID, 'DetailsPage_PrimeUpgradeGreyStripe_StaticText')
    unowned_tvod_grey_stripe_locator = (By.ID, 'DetailsPage_UnownedTvodGreyStripe_StaticText')
    detail_3p_logo_locator = (By.ID, 'DetailPage_3PLogo_Image')
    detail_prime_logo_locator = (By.ID, 'DetailPage_PrimeLogo_Image')
    xray_image_locator = (By.ID, 'DetailPage_XRayBadge_Image')

    imdb_person_from_imdb_locator = (By.ID, "IMDbPerson_SeeMoreAtIMDB_Button")
    imdb_person_header_locator = (By.ID, "IMDbPerson_Header_Cell")
    imdb_person_watch_othere_title_locator = (By.ID, "IMDbPerson_WatchOtherTitles_Cell")
    imdb_person_details_locator = (By.ID, "IMDbPerson_Details_Cell")
    imdb_person_see_more_at_imdb_locator = (By.ID, "IMDbPerson_SeeMoreAtIMDB_Button")

    @property
    def did_load(self):
        """
        :return: bool
        """
        return self.is_element_exist(self.synopsis_label_locator)

    @property
    def is_me(self):
        """
        :return: bool
        """
        return self.is_element_exist(self.synopsis_label_locator, timeout=3)

    @property
    def asin_title_cell(self):
        """
        :return: WebElement or None
        """
        if self.is_element_exist(self.detail_title_locator):
            table_cell = self.find_element(self.detail_title_locator)
            return table_cell.find_element(By.CLASS_NAME, 'UIAStaticText')
        return None

    @property
    def asin_title(self):
        """
        :return: str
        """
        title_cell = self.asin_title_cell
        if title_cell is not None and hasattr(title_cell, 'text'):
            return title_cell.text
        return ''

    @property
    def similar_titles_list(self):
        """
        :return: WebElement[]
        """
        if self.is_element_exist(self.detail_similar_titles_locator):
            similar_titles_container = self.find_element(self.detail_similar_titles_locator)
            similar_titles_buttons = similar_titles_container.find_elements_by_ios_uiautomation('.buttons()')
            return similar_titles_buttons
        return None

    @property
    def imdb_person_from_imdb(self):
        """
        return: WebElement or None
        """
        return self.find_element(self.imdb_person_from_imdb_locator)

    @property
    def imdb_person_description(self):
        """
        return: WebElement or None
        """
        header = self.find_element(self.imdb_person_header_locator)
        if header is None:
            return None

        static_text_list = header.find_elements(By.CLASS_NAME, "UIAStaticText")
        return static_text_list[1]

    @property
    def imdb_person_see_more(self):
        """
        return: WebElement or None
        """
        return self.find_element(self.imdb_person_see_more_at_imdb_locator)

    @property
    def imdb_person_watch_other_title_list(self):
        """
        return: WebElement or None
        """
        return self.find_element(self.imdb_person_watch_othere_title_locator).find_elements_by_ios_uiautomation('.buttons()')

    @property
    def imdb_person_details(self):
        """
        return: WebElement or None
        """
        return self.find_element(self.imdb_person_details_locator)

    @property
    def imdb_person_details_text(self):
        """
        :return: str
        """
        return AIVElement(self.imdb_person_details).value

    @property
    def alert_box(self):
        """
        :return: WebElement or None
        """
        return self.find_element(self.ui_alert_locator)

    def did_load_by_title(self, detail_page_title, timeout=10):
        """
        :param timeout -  in seconds:
        :param detail_page_title - title of the page to check:
        :return: bool
        """
        timeout_start = time.time()
        while time.time() < timeout_start + timeout:
            detailpage_asin_title = self.asin_title
            if detail_page_title in detailpage_asin_title or detailpage_asin_title in detail_page_title:
                return True
        return False

    def select_similar_title_by_index(self, index):
        """
        :param index: int
        :return: str
        """
        similar_title_button = self.similar_titles_list[index]
        similar_title_button.click()
        return similar_title_button.text

    def scroll_to_similar_titles(self):
        self.driver.aiv_action.scroll_to(*self.detail_similar_titles_locator)

    def scroll_to_cast_collection(self):
        if self.is_element_exist(self.cast_collection_locator):
            self.driver.aiv_action.scroll_to(*self.cast_collection_locator)

    def scroll_to_director(self):
        if self.is_element_exist(self.director_button_locator):
            self.driver.aiv_action.scroll_to(*self.director_button_locator)

    @property
    def cast_actors_list(self):
        """
        :return: list{UIAButton}
        """
        self.scroll_to_cast_collection()
        return self.find_element(self.cast_collection_locator).find_elements_by_ios_uiautomation('.buttons()')


    @property
    def actors(self):
        """
        :return: list{str}
        """
        for actor in self.cast_actors_list:
            if hasattr(actor, 'text') and actor.text != '':
                yield actor.text

    @property
    def director(self):
        """
        :return: str
        """
        self.scroll_to_cast_collection()
        director_label = self.find_element(self.director_button_locator).get_attribute('label')
        pos = re.search(': ', director_label).end()
        return director_label[pos:]

    @property
    def director_description(self):
        """
        :return: str
        """
        self.scroll_to_cast_collection()
        director_description = self.find_element(self.director_button_locator).get_attribute('hint')
        return director_description

    @property
    def see_more_at_imdb_button(self):
        """
        :return:UIAButton or None
        """
        return self.find_elements(self.see_more_at_imdb_button_locator)[-1]

    @property
    def see_full_cast_button(self):
        """
        :return:UIAButton or None
        """
        return self.find_element(self.see_full_cast_button_locator)

    @property
    def imdb_compact_rating_element(self):
        """
        :return:UIAElement or None
        """
        return self.find_element(self.imdb_compact_rating_locator)

    @property
    def imdb_rating_element(self):
        """
        :return:UIAElement or None
        """
        return self.find_element(self.imdb_rating_locator)

    def tap_how_do_I_watch_this_button(self):
        if self.is_element_exist(self.how_do_I_watch_this_locator):
            self.find_element(self.how_do_I_watch_this_locator).click()

    @property
    def how_do_I_watch_popup_text(self):
        """
        :return: str
        """
        if self.is_element_exist(self.ui_alert_locator):
            popup_text_elements = SharedSteps.find_element_by_chain(self, self.how_do_I_watch_popup_text_locator_chain, True)
            popup_text = next(popup_text_element for popup_text_element in popup_text_elements if popup_text_element.text != '')
            return popup_text.text

    @property
    def thirdparty_greystripe_text(self):
        """
        :return: str
        """
        if self.is_element_exist(self.thirdparty_greystripe_locator):
            return AIVElement(self.find_element(self.thirdparty_greystripe_locator)).aiv_text

    @property
    def prime_upgrade_greystripe_text(self):
        """
        :return: str
        """
        if self.is_element_exist(self.prime_upgrade_grey_stripe_locator):
            return AIVElement(self.find_element(self.prime_upgrade_grey_stripe_locator)).aiv_text

    @property
    def unowned_tvod_greystripe_text(self):
        """
        :return: str
        """
        if self.is_element_exist(self.unowned_tvod_grey_stripe_locator):
            return AIVElement(self.find_element(self.unowned_tvod_grey_stripe_locator)).aiv_text

    @property
    def third_party_logo(self):
        """
        :return:UIAImage or None
        """
        if self.is_element_exist(self.detail_3p_logo_locator):
            return self.find_element(self.detail_3p_logo_locator)
        else:
            return None

    @property
    def prime_logo(self):
        """
        :return:UIAImage or None
        """
        if self.is_element_exist(self.detail_prime_logo_locator):
            return self.find_element(self.detail_prime_logo_locator)
        else:
            return None

    def get_compact_rating(self):
        compact_rating_text = self.imdb_compact_rating_element.get_attribute('value')
        matcher = re.compile('([\d\.]+)W*out of.*')
        compact_rating = matcher.findall(compact_rating_text)[0]
        return compact_rating

    def get_rating(self):
        rating_text = self.imdb_compact_rating_element.get_attribute('value')
        matcher = re.compile('^(\d+\.\d+).*')
        ratings = matcher.findall(rating_text)
        rating = ratings[0]
        return rating

    def get_imdb_details_text(self):
        imdb_details_cell = self.driver.find_element(*self.imdb_details_locator)
        imdb_details_element = imdb_details_cell.find_element(*self.imdb_details_locator)
        imdb_details_text = imdb_details_element.get_attribute('value')
        return imdb_details_text

    @property
    def synopsis(self):
        """
        :return: WebElement or None
        """
        return self.find_element(self.synopsis_label_locator)

    @property
    def xray(self):
        """
        :return: WebElement or None
        """
        return self.find_element(self.xray_image_locator)

    def tap_thirdparty_how_do_I_watch_this_button(self):
        if self.is_element_exist(self.thirdparty_how_do_I_watch_this_locator):
            self.find_element(self.thirdparty_how_do_I_watch_this_locator).click()

    def tap_unowned_tvod_how_do_I_watch_this_button(self):
        if self.is_element_exist(self.how_do_I_watch_this_locator):
            self.find_element(self.how_do_I_watch_this_locator).click()

    def tap_watch_with_prime_button(self):
        if self.is_element_exist(self.watch_with_prime_locator):
            self.find_element(self.watch_with_prime_locator).click()

    def type_pin(self, pin):
        """
        :param pin: str
        """
        if not self.__is_pin_corrected_typed(pin):
            Logger.debug('pin is digital only.')
            return

        if self.alert_box is not None:
            pin_field = self.find_element_by_chain(self.pin_secure_text_field_locator_chain)
            pin_field.send_keys(str(pin))
            self.accept_alert()

    def __is_pin_corrected_typed(self, pin):
        """
        :param pin: str
        :return: bool
        """
        return re.match('\d+', str(pin)) is not None
