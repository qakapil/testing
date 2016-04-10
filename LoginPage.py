from selenium.webdriver.common.by import By

from Model.Page import Page
from library.driver.SharedSteps import SharedSteps


class LoginPage(Page):
    def __init__(self, driver):
        Page.__init__(self, driver)

    sign_in_locator_chain = [(By.CLASS_NAME, 'UIAScrollView'), (By.NAME, 'Sign In')]
    username_locator = (By.NAME, 'email or mobile number')
    password_locator = (By.NAME, 'password')
    sign_in_error_popup_locator = (By.CLASS_NAME, 'UIAAlert')
    challenge_popup_navigation_bar_locator = (By.NAME, 'Amazon.com Sign In')
    web_view_popup_locator = (By.CLASS_NAME, 'UIAWebView')
    beta_access_error_message_locator_chain = [sign_in_error_popup_locator, (By.CLASS_NAME, 'UIAStaticText')]
    not_beta_user_message = "You are not a beta tester"

    @property
    def did_load(self):
        """
        :return: bool
        """
        element_list = [self.username_locator, self.password_locator]
        return SharedSteps.aiv_are_elements_exist(self.driver, element_list, timeout=15)

    @property
    def is_me(self):
        """
        :return: bool
        """
        return SharedSteps.aiv_is_element_exist(self.driver, *self.password_locator, timeout=5)

    @property
    def is_challenged(self):
        """
        :return: bool
        """
        return SharedSteps.aiv_is_element_exist(self.driver, *self.challenge_popup_navigation_bar_locator)

    @property
    def username_textfield(self):
        """
        :return: WebElement
        """
        return self.driver.find_element(*self.username_locator)

    @property
    def password_textfield(self):
        """
        :return: list[WebElement]
        """
        return self.driver.find_element(*self.password_locator)

    @property
    def sign_in_button(self):
        """
        :return: WebElement
        """
        sign_in_button_list = SharedSteps.find_element_by_chain(self, self.sign_in_locator_chain, True)
        for element in sign_in_button_list:
            if element.is_displayed():
                return element

    @property
    def sign_in_error_popup(self):
        """
        :return: WebElement or None
        """
        return self.find_element(self.sign_in_error_popup_locator)


    @property
    def sign_in_challenge_popup(self):
        """
        :return: WebElement or None
        """
        if self.challenge_popup_navigation_bar is not None:
            return self.find_element(self.web_view_popup_locator)
        return None

    @property
    def challenge_popup_navigation_bar(self):
        """
        :return: WebElement or None
        """
        return self.find_element(self.challenge_popup_navigation_bar_locator)

    @property
    def has_beta_access_error_message(self):
        """
        :retrun bool
        """
        text_nodes = SharedSteps.find_element_by_chain(self, self.beta_access_error_message_locator_chain, True)
        if text_nodes is not None:
            return text_nodes[1].name == self.not_beta_user_message
        return False

    def press_sign_in(self):
        self.sign_in_button.click()

    def login_with_credential(self, username, password):
        self.username_textfield.clear()
        self.username_textfield.send_keys(username)
        self.password_textfield.clear()
        self.password_textfield.send_keys(password)






