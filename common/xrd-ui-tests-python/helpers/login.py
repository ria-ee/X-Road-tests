import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
import view_models.login as login_constants


def login(self, username, password, login_with_enter=False):
    """
    Try to log in to a server (central or security) with the specified username and password.
    :param self: MainController class object
    :param username: str - Username to log in with
    :param password: str - Password to log in with
    :param login_with_enter: bool - send "Enter" key instead of clicking the login button
    :return: bool - True if login succeeded or already logged in; False otherwise
    """
    logged_in = check_login(self, username)
    if logged_in:
        if self.debug:
            self.log('Already logged in')
        return True

    if self.debug:
        self.log("We haven't tried to log in, check_login value: {0}".format(logged_in))
    input_username = self.wait_until_visible(type=By.ID, element=login_constants.USERNAME_AREA)
    input_password = self.wait_until_visible(type=By.ID, element=login_constants.PASSWORD_AREA)

    self.input(input_username, username)
    self.input(input_password, password)

    # If we are instructed to login with enter, send "Enter" keypress to password field - that's what a user would do.
    if login_with_enter:
        self.input(input_password, Keys.ENTER)
    # Otherwise we log in by looking up the login button (submit button) and clicking it.
    else:
        login_button = self.wait_until_visible(type=By.XPATH, element=login_constants.SUBMIT_BUTTON)
        login_button.click()

    if self.debug:
        self.log("We have tried to log in, check_login value: {0}".format(check_login(self, username)))

    if not check_login(self, username, wait=True):
        # Try to check if an error message was shown
        try:
            error_message = self.wait_until_visible(type=By.CSS_SELECTOR,
                                                    element=login_constants.LOGIN_ERROR_MESSAGE_CSS)
            if error_message.is_displayed():
                self.log("XRoad login error: {0}".format(error_message.text))
        except (NoSuchElementException, TimeoutException):
            # Element not found, pass (we raise an exception later)
            pass

        raise RuntimeError("Cannot find user menu, login failed.")

    return True


def check_login(self, username, wait=False):
    """
    Check if user is already logged in (field visible and username matches)
    :param self: MainController class object
    :param username: str - check for login username
    :return: bool - True if logged in and username matches; False otherwise

    """
    try:
        # Get the username field
        if wait:
            user_info = self.wait_until_visible(element=login_constants.LOGIN_USERNAME_VALUE_CSS, type=By.CSS_SELECTOR)
        else:
            user_info = self.by_css(element=login_constants.LOGIN_USERNAME_VALUE_CSS)
        # Check if username matches.
        if user_info.text.strip() == username:
            return True
        else:
            return False
    # Exception has been raised, therefore the element was not found
    except NoSuchElementException:
        return False


def logout(self, url=None):
    """
    Log out by going to logout URL.
    :param self: MainController class object
    :param url: host where logout is needed, string
    :return: None
    """

    if url is None:
        self.go(self.url)
        time.sleep(3)
        user_info = None
        try:
            user_info = self.by_css(element=login_constants.LOGIN_USERNAME_VALUE_CSS)
        except:
            pass

        if user_info is not None:
            # Get the driver to go to logout URL. Fails if no driver is present.
            self.go('{0}{1}'.format(self.url, login_constants.LOGOUT_URL))
        else:
            self.go('{0}'.format(self.url))
    else:
        self.go(url)
        time.sleep(3)
        user_info = None
        try:
            user_info = self.by_css(element=login_constants.LOGIN_USERNAME_VALUE_CSS)
        except:
            pass
        if user_info is not None:
            # Get the driver to go to logout URL. Fails if no driver is present.
            self.go('{0}{1}'.format(url, login_constants.LOGOUT_URL))
        else:
            self.go('{0}'.format(url))
