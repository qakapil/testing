from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from Model.Page import Page
from library.driver.SharedSteps import SharedSteps
from library.config_manager import ConfigManager
from library.driver.SharedAction import SharedAction
from library.utilities.extensions import AIVElement
from library.logger import Logger
from library import Constant
from time import sleep


class PlaybackPage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)
        self._mid_x = self.driver.get_window_size().get('width') / 2
        self._mid_y = self.driver.get_window_size().get('height') / 2
        # TODO: 187 is the magic number here. A good fix should be in https://jira-int.amazondcl.com/browse/AIVIOS-5028
        self._backward_ten_x = self._mid_x - 187
        self._forward_ten_x = self._mid_x + 187

    player_frame_locator = (By.NAME, 'AIVPlayerViewController')
    playcontrol_play_locator = (By.NAME, 'Play')
    playcontrol_pause_locator = (By.NAME, 'Pause')
    caption_button_locator = (By.NAME, 'Audio and closed captions options')
    text_node_locator = (By.CLASS_NAME, 'UIAStaticText')
    done_button_locator = (By.ID, 'PlayerControls_Done_Button')
    video_element_locator = (By.NAME, 'Video')
    #Bottom player controls
    slider_bars_locator = (By.CLASS_NAME, 'UIASlider')
    playhead_position_locator = (By.ID, 'PlayerControls_playheadPosition_Text')
    content_duration_locator = (By.ID, 'PlayerControls_contentDuration_Text')
    credit_start_time_locator = (By.ID, 'PlayerDebug_CreditStartTime_Text')
    next_up_card_element_locator = (By.ID, 'NextUpCard_Element')


    xray_quickview_open_xray_button_locator = (By.ID, "XrayQuickView_OpenXray_Button")

    @property
    def did_load(self):
        """
        :return: bool
        """
        if self.is_me:
            retry = 0
            self.tap_somewhere()
            while retry < int(ConfigManager().retrieve_config_value('driver', 'retries')):
                if self.play_button is None:
                    self.tap_somewhere()
                    if self.play_button is not None:
                        return True
                    else:
                        retry += 1
                else:
                    return True
        return False

    @property
    def is_me(self):
        """
        :return: bool
        """
        return self.is_element_exist(self.playcontrol_play_locator) or self.is_element_exist(self.player_frame_locator) or self.is_element_exist(self.video_element_locator)

    @property
    def current_title(self):
        """
        :return: str
        """
        self.make_player_controls_visible_pause()
        static_text_node_list = self.find_elements(self.text_node_locator)
        # TODO: This is assuming play title always 3rd after "Skip" text label,
        # we need to find a more reliable way to find which static text is what we want.
        # Talk to dev team to give a more predictable label for this.
        for index, node in enumerate(static_text_node_list):
            if node.text == 'Skip':
                return static_text_node_list[index + 3].text
        return ''

    @property
    def episode_info(self):
        """
        :return: str
        """
        self.make_player_controls_visible_pause()
        static_text_node_list = self.find_elements(self.text_node_locator)
        # TODO: This is assuming episode information always 4th after "Skip" text label,
        # we need to find a more reliable way to find which static text is what we want.
        # Talk to dev team to give a more predictable label for this.
        for index, node in enumerate(static_text_node_list):
            if node.text == 'Skip':
                return static_text_node_list[index + 4].text
        return ''

    @property
    def player_slider(self):
        """
        :return: WebElement or None
        """
        self.tap_somewhere()
        return self.find_elements(self.slider_bars_locator)[-1]

    @property
    def playtime_percentage(self):
        """
        :return: str
        """
        return self.player_slider.get_attribute('value')

    @property
    def play_button(self):
        """
        :return: WebElement or None
        """
        return self.find_element(self.playcontrol_play_locator)

    @property
    def pause_button(self):
        """
        :return: WebElement or None
        """
        return self.find_element(self.playcontrol_pause_locator)

    @property
    def done_button(self):
        """
        :return: WebElement or None
        """
        return self.find_element(self.done_button_locator)

    @property
    def caption_button(self):
        """
        :return: WebElement or None
        """
        return self.find_element(self.caption_button_locator)

    @property
    def is_player_control_visible(self):
        """
        :return: bool
        """
        return SharedSteps.aiv_is_element_exist(self.driver, *self.slider_bars_locator)

    @property
    def playtime_in_seconds(self):
        """
        :return: str
        """
        self.make_player_controls_visible_pause()
        static_text_node_list = self.find_elements(self.text_node_locator)
        # TODO: This is assuming playtime always after "Skip" text label,
        # we need to find a more reliable way to find which static text is what we want.
        # Talk to dev team to give a more predictable label for playtime element.
        for index, node in enumerate(static_text_node_list):
            if node.text == 'Skip':
                return static_text_node_list[index + 1].text
        return ''


    def tap_centre(self):
        mid_x = self.driver.get_window_size().get('width') / 2
        mid_y = self.driver.get_window_size().get('height') / 2
        self.driver.tap([(mid_x, mid_y)], duration=200)


    def tap_somewhere(self):
        random_point = [(300, 20)]
        self.driver.tap(random_point, duration=300)


    def tap_above_play_button(self):
        offsetY = 125
        mid_x = self.driver.get_window_size().get('width') / 2
        mid_y = self.driver.get_window_size().get('height') / 2
        mid_y = mid_y + offsetY
        self.tap_specific_point([(mid_x, mid_y)])


    def tap_specific_point(self, point):
        self.driver.tap(point, duration=200)


    def next_up_element_location(self):
        """
        :return: point
        """
        next_up_locator = self.next_up_card_element
        next_up_element_width = next_up_locator.size['width']
        next_up_element_height = next_up_locator.size['height']
        offsetx = next_up_element_width/2
        offsety = next_up_element_height/2
        next_up_element_x = next_up_locator.location['x'] + offsetx
        next_up_element_y = next_up_locator.location['y'] + offsety
        point = [(next_up_element_x,  next_up_element_y)]
        return point


    def make_player_controls_visible_pause(self):
        retry = 0
        while not self.is_player_control_visible and retry < int(
                ConfigManager().retrieve_config_value('driver', 'retries')):
            self.tap_somewhere()
            if self.is_player_control_visible:
                self.click_caption_icon()
                break
            else:
                retry += 1
        else:
            self.click_caption_icon()

    def click_caption_icon(self):
        try:
            if self.caption_button is not None:
                self.caption_button.click()
        except WebDriverException:
            pass

    def tap_skip_10_seconds(self, direction):
        """
        :param direction: forward or backward
        """
        if direction.lower() == 'forward':
            self.driver.tap([(self._forward_ten_x, self._mid_y)], 200)
        if direction.lower() == 'backward':
            self.driver.tap([(self._backward_ten_x, self._mid_y)], 200)

    def quit_playback(self):
        self.make_player_controls_visible_pause()
        self.tap_somewhere()
        SharedAction.click_button_if_exist(self.driver, 'Close')#for iPhone
        self.click_button(self.done_button_locator[-1])

    @property
    def content_duration(self):
        """
        return: WebElement or None
        """
        return self.find_element(self.content_duration_locator)

    @property
    def content_duration_value_text(self):
        return AIVElement(self.content_duration).aiv_text

    @property
    def credit_start_time(self):
        """
        return: WebElement or None
        """
        return self.find_element(self.credit_start_time_locator)

    @property
    def credit_start_time_value_text(self):
        return AIVElement(self.credit_start_time).aiv_text


    #/Use a similar function to this to calculate perfentage to scroll the slider
    def parse_credit_start_time(self, credit_start_time):
        """
        :param credit_start_time:
        :return str
        """
        minute = credit_start_time.split(':')[1]
        second = credit_start_time.split(':')[2]
        parsed = minute+':'+second
        return parsed

    def convert_time_to_seconds(self, play_time):
        """
        :param play_time:
        :return: int
        """
        minute = play_time.split(':')[0]
        second = play_time.split(':')[1]
        return int(minute) * 60 + int(second)


    def calculate_percentage_to_move_slider(self, credit_start_time_seconds, content_duration_time_seconds):
        """
        :param credit_start_time_seconds:
        :param content_duration_time_seconds:
        :return: float
        """
        slider_percentage = float(float(credit_start_time_seconds)/float(content_duration_time_seconds))
        return slider_percentage


    def scrub_to_new_time(self, percentage):
        startX = int(self.player_slider.location['x']) + 2
        startY = int(self.player_slider.location['y'])
        offsetX = float(self.player_slider.size['width']) * percentage
        self.driver.aiv_action.swipe(startX, startY, offsetX, 0)


    def scrub_to_credits_start_time(self):
        self.scrub_to_new_time(0)
        credit_start_time = self.credit_start_time_value_text
        credit_start_time_parse = self.parse_credit_start_time(credit_start_time)
        credit_start_time_seconds = self.convert_time_to_seconds(credit_start_time_parse)
        content_duration_time = self.content_duration_value_text
        content_duration_time_seconds = self.convert_time_to_seconds(content_duration_time)
        percentage = self.calculate_percentage_to_move_slider(credit_start_time_seconds, content_duration_time_seconds)
        percentage = percentage - Constant.player_slider_scrub_offset
        self.scrub_to_new_time(percentage)


    @property
    def slider(self):
        return self.find_element(self.slider_bars_locator)


    @property
    def slider_bars_value(self):
        return AIVElement(self.slider).value


    @property
    def next_up_card_element(self):
       return self.find_element(self.next_up_card_element_locator)


    def navigate_to_xray(self):
         self.find_element(self.xray_quickview_open_xray_button_locator).click()

