from selenium.webdriver.common.by import By

from Model.DetailsBasePage import DetailsBasePage


class MovieDetailsPage(DetailsBasePage):
    def __init__(self, driver):
        DetailsBasePage.__init__(self, driver)

    movie_details_label_locator = (By.NAME, 'Movie Details')
    movie_detail_watch_button_locator = (By.NAME, 'Watch Now')
    movie_detail_resume_button_locator = (By.NAME, 'Resume')
    movie_detail_play_trailer_locator = (By.NAME, 'Play Trailer')
    download_button_name = 'Download'
    notification_ok_button_name = 'OK'

    @property
    def did_load(self):
        if super(MovieDetailsPage, self).did_load:
            # TODO: Add IDs around the synopsis this is a quick work around to complete this story
            return self.is_movie_synopsis

    @property
    def is_me(self):
        if super(MovieDetailsPage, self).is_me:
            # TODO: Add IDs around the synopsis this is a quick work around to complete this story
            return self.is_movie_synopsis

    @property
    def watch_button(self):
        return self.find_element(self.movie_detail_watch_button_locator)

    @property
    def resume_button(self):
        return self.find_element(self.movie_detail_resume_button_locator)

    @property
    def play_trailer_button(self):
        return self.find_element(self.movie_detail_play_trailer_locator)

    @property
    def is_movie_synopsis(self):
        if self.find_element(self.movie_details_label_locator) is not None: #iPad only
            return True

        movie_synopsis = self.synopsis
        print("M"*10)
        print(movie_synopsis)
        if movie_synopsis is not None:
            value = movie_synopsis.get_attribute('value')
            print(value)
            if 'Movie Details' in value:
                return True
        return False

    def play_title(self):
        if self.watch_button is not None:
            self.watch_button.click()
        else:
            self.resume_button.click()

    def play_trailer(self):
        self.play_trailer_button.click()

    def start_download(self):
        self.click_button(self.download_button_name)
        if self.is_element_exist((By.NAME, self.notification_ok_button_name)):
            self.click_button(self.notification_ok_button_name)
