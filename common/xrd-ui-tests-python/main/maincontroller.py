# coding=utf-8
from __future__ import absolute_import

import os, errno
import sys
import traceback
from datetime import datetime
import shutil
import inspect

import selenium.webdriver.support.expected_conditions as conditions
import selenium.webdriver.support.ui as ui
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from helpers import confreader, webdriver_init, mockrunner, login
from main.assert_helper import AssertHelper

from selenium.webdriver.common.action_chains import ActionChains


class MainController(AssertHelper):
    # Default configuration file, relative to our current script
    configuration = 'config.ini'

    close_webdriver = True  # Close webdriver in tearDown
    driver = None  # Init webdriver variable
    driver_type = webdriver.Firefox  # Webdriver type, currently only Firefox is supported
    driver_autostart = False  # Autostart webdriver in setUp
    mock_service = None  # Init mock service variable
    mock_service_autostart = False  # Autostart mock service
    disable_mock_service = False  # Disable mock service
    username = None  # Default username
    password = None  # Default password
    url = ''  # Default url
    debug = True  # Show debug messages

    # MainController path (../ relative from maincontroller.py location)
    main_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

    # Working directory script path
    working_dir = os.path.normpath(os.getcwd())

    # Check if configuration is not an absolute path
    if configuration is not None and not os.path.isabs(configuration):
        configuration = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), configuration))
    # If default configuration file does not exist, no default config will be loaded.
    if not os.path.isfile(configuration):
        configuration = None

    # Init config
    config = confreader.ConfReader(ini_path=configuration, init_command_line=True)

    # Default settings
    save_exceptions = True
    save_screenshots = True
    temp_dir = 'temp'
    download_dir = 'temp/downloads'
    mock_cert_path = 'mock/certs'
    mock_query_path = 'mock/queries'

    # Browser log. Relative to main_path or absolute.
    browser_log = 'firefox_console.txt'

    empty_download_directory = True
    create_directories = True

    test_number = ''  # Test number (eg 2.2.1)
    test_name = ''  # Test name (eg "System test")

    def __init__(self, case):
        '''
        Initialize the class.

        :param case: TestCase - the current testcase that is running, used for assertions
        '''
        # Init AssertHelper
        AssertHelper.__init__(self, case)

        # Check if custom configuration files are allowed to be loaded from the current working directory.
        if self.config.get_bool('config.load_custom_config', True):
            # If there are additional configuration files in the working directory, load them
            config_file = os.path.join(self.working_dir, 'config.kvp')
            if os.path.isfile(config_file):
                self.config.read_key_value_pairs(config_file)
            config_file = os.path.join(self.working_dir, 'config.ini')
            if os.path.isfile(config_file):
                self.config.read_ini(config_file)
            config_file = os.path.join(self.working_dir, 'config.json')
            if os.path.isfile(config_file):
                self.config.read_json(config_file)

        # Set debug; if not set, use default value
        self.debug = self.config.get_bool('config.debug', self.debug)

        # Save exception data and tracebacks as text files to 'temp/'
        self.save_exceptions = self.config.get_bool('config.save_exceptions', self.save_exceptions)
        # Save screenshots as .png files to 'temp/'
        self.save_screenshots = self.config.get_bool('config.save_screenshots', self.save_screenshots)

        # Temp, download, mock cert and query paths. Can be relative to main_path or absolute paths.
        self.temp_dir = self.get_path(self.config.get_string('config.temp_dir', self.temp_dir))
        self.download_dir = self.get_path(self.config.get_string('config.download_dir', self.download_dir))
        self.mock_cert_path = self.get_path(self.config.get_string('config.certs_dir', self.mock_cert_path))
        self.mock_query_path = self.get_path(self.config.get_string('config.query_dir', self.mock_query_path))

        # Browser log. Relative to main_path or absolute.
        self.browser_log = self.get_path(self.config.get_string('config.browser_log', self.browser_log))

        self.empty_download_directory = self.config.get_bool('config.empty_download_dir', self.empty_download_directory)
        self.create_directories = self.config.get_bool('config.create_directories', self.create_directories)

        self.disable_mock_service = not self.config.get_bool('mockrunner.enabled', True)

        used_dirs = [self.temp_dir, self.download_dir, self.mock_cert_path, self.mock_query_path]

        # Create directories that do not already exist
        if self.create_directories:
            for new_dir in used_dirs:
                try:
                    os.makedirs(new_dir)
                except OSError as exc:
                    if exc.errno == errno.EEXIST and os.path.isdir(new_dir):
                        # If the directory already exists, do nothing
                        pass
                    else:
                        # Something else, raise an Exception
                        raise

        if self.debug:
            self.log('Default configuration: {0}'.format(self.configuration))
            self.log('INI file: {0}'.format(self.config.get('ini')))
            self.log('JSON file: {0}'.format(self.config.get('json')))
            self.log('Config file: {0}'.format(self.config.get('config')))
            self.log('Base directory: {0}'.format(self.get_path()))
            self.log('Temporary directory: {0}'.format(self.get_temp_path()))
            self.log('Download directory: {0}'.format(self.get_download_path()))
            self.log('Mock client certificates directory: {0}'.format(self.get_cert_path()))
            self.log('Query XML directory: {0}'.format(self.get_query_path()))

        if self.empty_download_directory:
            self.log('Clearing download directory')
            self.empty_directory(self.get_download_path())

        # set up test environment
        self.setUp()

    def setUp(self):
        '''
        Test setUp method.
        :return: None
        '''

        # Start WebDriver if autostart enabled
        if self.driver_autostart:
            self.reset_webdriver(url=self.url, username=self.username, password=self.password)

        # Start MockRunner if autostart enabled
        if self.mock_service_autostart:
            self.start_mock_service()

    def tearDown(self, save_exception=True):
        '''
        Test tearDown method, used for closing the test environment after successful or failed tests.
        :param save_exception: bool - True to save exception data; False otherwise
        :return: None
        '''

        # If we have mock service up and running, stop it.
        if self.mock_service is not None:
            self.mock_service.stop()

        if save_exception:
            # Save exception data if there is any
            self.save_exception_data()

        # If WebDriver instance exists
        if self.driver is not None:
            # Close the driver
            if self.close_webdriver:
                # self.driver.close()
                self.driver.quit()

    def save_exception_data(self, exctype=None, excvalue=None, exctrace=None):
        """
        Saves the exception screenshot and traceback if set in configuration.
        :return: None
        """

        # Do we need to save anything about errors?
        if self.save_exceptions or self.save_screenshots:
            if exctype is None and excvalue is None and exctrace is None:
                # Is there an error at all?
                if sys.exc_info()[0]:
                    # Get exception type, textual value and traceback
                    exctype, excvalue, exctrace = sys.exc_info()
                    exctype = exctype.__name__
                    exctrace = traceback.format_exc()

            if exctype is not None or excvalue is not None or exctrace is not None:
                # Test method name can be set to reflect the test.
                test_method_name = self.test_name

                # Create timestamp YYYYMMDDHHmmss
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

                # Check if WebDriver was up and running
                if self.driver is not None:
                    # Save screenshot
                    if self.save_screenshots:
                        screenshot_filename = 'error_{0}_{1}.png'.format(test_method_name, timestamp)
                        screenshot_fullpath = self.save_screenshot(screenshot_filename)
                        self.log(
                            'Error in {0} ({1}), screenshot saved to: {2}'.format(test_method_name, self.test_number,
                                                                                  screenshot_fullpath))

                # Save exception data with traceback to text file
                if self.save_exceptions:
                    exception_filename = 'error_{0}_{1}.txt'.format(test_method_name, timestamp)

                    # Create string to be saved to the file, use exception class, value and traceback as text
                    exception_data = '{0} {1}\n{2}: {3}\n{4}'.format(self.test_number, self.test_name,
                                                                     exctype, excvalue,
                                                                     exctrace)

                    text_fullpath = self.save_text_data(exception_filename, exception_data)

                    self.log('Error in {0} ({1}), data saved to: {2}'.format(test_method_name, self.test_number,
                                                                             text_fullpath))

    def get_path(self, path=''):
        '''
        Gets the absolute path from base path and path variable; or returns path if it is absolute.
        :param path: str - relative path to base path; if path is absolute, nothing else is computed
        :return: str - absolute path
        '''
        # If path is absolute, return it
        if os.path.isabs(path):
            return os.path.normpath(path)
        # Otherwise assume it is relative and return it joined with main path
        return os.path.normpath(os.path.join(self.main_path, path))

    def get_temp_path(self, path=''):
        '''
        Returns the temporary directory with additional path if specified. Returns only path if path variable is
        an absolute path.
        :param path: str - path relative to temporary directory; or absolute path if specified
        :return: str - absolute path
        '''
        # If path is absolute, return it
        if os.path.isabs(path):
            return path
        return os.path.normpath(os.path.join(self.get_path(self.temp_dir), path))

    def get_query_path(self, path=''):
        '''
        Returns the mock query directory with additional path if specified. Returns only path if path variable is
        an absolute path.
        :param path: str - path relative to temporary directory; or absolute path if specified
        :return: str - absolute path
        '''
        # If path is absolute, return it
        if os.path.isabs(path):
            return path
        return os.path.normpath(os.path.join(self.get_path(self.mock_query_path), path))

    def get_cert_path(self, path=''):
        '''
        Returns the certificate directory with additional path if specified. Returns only path if path variable is
        an absolute path.
        :param path: str - path relative to temporary directory; or absolute path if specified
        :return: str - absolute path
        '''
        # If path is absolute, return it
        if os.path.isabs(path):
            return path
        return os.path.normpath(os.path.join(self.get_path(self.mock_cert_path), path))

    def get_download_path(self, path=''):
        '''
        Returns the download directory with additional path if specified. Returns only path if path variable is
        an absolute path.
        :param path: str - path relative to temporary directory; or absolute path if specified
        :return: str - absolute path
        '''
        # If path is absolute, return it
        if os.path.isabs(path):
            return path
        return os.path.normpath(os.path.join(self.get_path(self.download_dir), path))

    def empty_directory(self, path):
        '''
        Empties a directory of any files and subdirectories (recursively). Failures are logged but exceptions are
        not raised. Directory itself is not removed.
        :param path: parent directory
        :return: None
        '''
        for root, dirs, files in os.walk(top=self.get_download_path()):
            for filename in files:
                file_path = os.path.join(root, filename)
                try:
                    os.remove(file_path)
                except:
                    self.log('Failed to delete {0}'.format(file_path))
            for dirname in dirs:
                dir_path = os.path.join(root, dirname)
                try:
                    shutil.rmtree(dir_path, ignore_errors=True)
                except:
                    self.log('Failed to delete {0}'.format(dir_path))

    def remove_files(self, file_list, remove_directories=True):
        '''
        Removes files and, if instructed, directories given in a list. These must be given as absolute paths.
        Directories do not have to be empty to be removed.
        :param file_list: [str]|str - Single path as string or list of paths to remove.
        :param remove_directories: bool - remove directories, not only files
        :return: bool - True if everything was deleted; False is there was at least one error.
        '''
        for filename in file_list:
            result = True
            if not os.path.isabs(filename):
                self.log('Not deleting relative path: {0}'.format(filename))
                result = False
                continue
            if os.path.isdir(filename):
                if remove_directories:
                    try:
                        shutil.rmtree(filename, ignore_errors=True)
                    except:
                        self.log('Failed to delete {0}'.format(filename))
                        result = False
                else:
                    self.log('Failed to delete directory: {0}'.format(filename))
                    result = False
            else:
                try:
                    os.remove(filename)
                except:
                    self.log('Failed to delete {0}'.format(filename))
                    result = False
        return result

    def get_xml_query(self, filename):
        '''
        Reads an XML query data from a file.
        :param filename: str - filename
        :return: str - file contents
        '''
        file_path = self.get_query_path(filename)

        with open(file_path, 'r') as f:
            return f.read()

    def reset_webdriver(self, url, username=None, password=None, close_previous=True, init_new_webdriver=True):
        '''
        Resets the webdriver to a specified url.
        :param url: str - URL to open
        :param username: str|None - if specified, try to log in
        :param password: str|None - password used with the username
        :param close_previous: bool - if True, close the current webdriver instance if it exists
        :param init_new_webdriver: bool - if True, always open a new webdriver instance
        :return: None
        '''

        # Close the current WebDriver instance if it exists and we're asked to do so.
        if close_previous and self.driver is not None:
            self.driver.quit()
            self.driver = None

        # If WebDriver does not exist or we're asked to open a new instance, do it.
        if init_new_webdriver or self.driver is None:
            try:
                self.driver = webdriver_init.get_webdriver(self.driver_type, download_dir=self.get_download_path(),
                                                           log_dir=self.get_temp_path(self.browser_log))
            except:
                # If WebDriver fails to start, the test has failed.
                assert False, 'MainController: failed to start WebDriver'

        try:
            # Go to URL
            self.driver.get(url)
        except:
            assert False, 'MainController: WebDriver failed, URL: '.format(url)

        # If username specified, try to log in
        if username is not None:
            self.login(username=username, password=password)

        # Set internal variables
        self.url = url
        self.username = username
        self.password = password

    def reload_webdriver(self, url, username=None, password=None):
        '''
        Reloads the webdriver with the specified URL, without opening or closing anything.
        :param url: str - URL to open
        :param username: str|None - if specified, try to log in
        :param password: str|None - password used with the username
        :return: None
        '''
        self.reset_webdriver(url=url, username=username, password=password, close_previous=False,
                             init_new_webdriver=False)

    def start_mock_service(self):
        '''
        Starts a mock service using SSH.
        :return: None
        '''

        # If mock service is disabled, write a message to log and do nothing else.
        if self.disable_mock_service:
            self.log('Mock service starter disabled. Service needs to be already started for the tests to succeed.')
        else:
            # If mock service class has not been instantiated, do it now with settings specified in configuration.
            if self.mock_service is None:
                if self.debug:
                    self.log('Creating MockRunner')
                self.mock_service = mockrunner.MockRunner(self.config.get('mockrunner.ssh_host'),
                                                          self.config.get('mockrunner.ssh_user'),
                                                          self.config.get('mockrunner.ssh_pass'),
                                                          self.config.get('mockrunner.service_command'),
                                                          ready_regex=self.config.get(
                                                              'mockrunner.service_running_regex'))
            # Start the service
            self.mock_service.start()

    def save_screenshot(self, filename):
        '''
        Saves a screenshot of the WebDriver window to temporary directory.
        :param filename: str - filename of the screenshot
        :return: str - filename
        '''

        try:
            # Get screenshot absolute path
            screenshot_fullpath = self.get_temp_path(filename)

            self.driver.save_screenshot(screenshot_fullpath)

            # Return file path
            return screenshot_fullpath
        except:
            return None

    def save_text_data(self, filename, data):
        '''
        Saves text data (usually the exception traceback and message) to a file.
        :param filename: str - filename of the screenshot
        :param data: str - file contents
        :return: str - filename
        '''

        try:
            # Get text file absolute path
            text_fullpath = self.get_temp_path(filename)

            # Open and write to file
            f = open(text_fullpath, 'w')
            f.write(data)
            # Close the file
            f.close()

            # Return file path
            return text_fullpath
        except:
            return None

    def logout(self, url=None):
        '''
        Logout function, logs the user out.
        :param url: string, url where logout is wanted
        :return: None
        '''
        return login.logout(self=self, url=url)

    def login(self, username, password):
        '''
        Login function. Tries to log in with the specified credentials.
        :param username: str - login username
        :param password: str - login password
        :return: bool - True if login successful or already logged in; False otherwise
        '''
        return login.login(self=self, username=username, password=password)

    def by_id(self, element):
        """
        Searches for and returns a WebElement using element ID
        :param element: str - element ID
        :return: WebDriverElement|[WebDriverElement] - element(s) found
        """
        return self.driver.find_element_by_id(element)

    def by_xpath(self, element, multiple=False):
        """
        Searches for and returns WebElement(s) (depending on if multiple is True or False) using XPATH
        :param element: str - XPath selector
        :param multiple: bool - True to return multiple elements; False to return the first one
        :return: WebDriverElement|[WebDriverElement] - element(s) found
        """
        if multiple:
            return self.driver.find_elements_by_xpath(element)
        else:
            return self.driver.find_element_by_xpath(element)

    def by_css(self, element, multiple=False):
        """
        Searches for and returns WebElement(s) (depending on if multiple is True or False) using CSS selector
        :param element: str - CSS selector
        :param multiple: bool - True to return multiple elements; False to return the first one
        :return: WebDriverElement|[WebDriverElement] - element(s) found
        """
        if multiple:
            return self.driver.find_elements_by_css_selector(element)
        else:
            return self.driver.find_element_by_css_selector(element)

    def wait(self, condition, timeout=120):
        """
        Waits until a specified condition is true.
        :param condition: Condition - condition to wait for
        :param timeout: int - timeout in seconds
        :return: None
        """
        driver_wait = WebDriverWait(self.driver, timeout)
        driver_wait.until(condition)

    def wait_until_visible(self, element, type=None, timeout=10, multiple=False):
        """
        Waits until an element (or elements if multiple is True) is visible or timeout occurs, then returns the
         element(s). Element parameter can be a WebElement or a string in combination with type parameter that specifies
         the type of the query.
        :param element: WebDriverElement|str - element to be waited for; if type specified, the lookup string of the element
        :param type: type of the element to be looked for, comes from WebDriver By class
        :param timeout: int - how long are we trying to wait for the elements
        :param multiple: bool - True to return multiple elements; False to return the first one
        :return: WebDriverElement|[WebDriverElement] - element(s) found
        """
        if type is None:
            ui.WebDriverWait(self.driver, timeout=timeout).until(conditions.visibility_of(element))
        else:
            ui.WebDriverWait(self.driver, timeout=timeout).until(
                conditions.visibility_of_element_located((type, element)))
            if multiple:
                element = self.driver.find_elements(type, element)
            else:
                element = self.driver.find_element(type, element)
        return element

    def js(self, script, *args):
        '''
        Execute JavaScript in the WebDriver instance.
        :param script: str - JavaScript string
        :param args: mixed - arguments
        :return: mixed - result from executing the script
        '''
        if self.debug:
            self.log('Executing JS: {0}'.format(script))
        return self.driver.execute_script(script, *args)

    def async_js(self, script, *args):
        '''
        Execute JavaScript asynchronously (non-blocking) in the WebDriver instance.
        :param script: str - JavaScript string
        :param args: mixed - arguments
        :return: mixed - result from executing the script
        '''
        if self.debug:
            self.log('Executing async JS: {0}'.format(script))
        return self.driver.execute_async_script(script, *args)

    def wait_jquery(self, timeout=120):
        """
        Waits until jQuery.ajax request is finished (or timeout), then gives control back to the program.
        :param timeout: int - maximum time in seconds to wait
        :return: None
        """
        if self.debug:
            self.log('Waiting for AJAX to load the data')
        return self.wait(lambda driver: driver.execute_script("return jQuery.active == 0"), timeout=timeout)

    def get_classes(self, element):
        """
        Returns element classes as a list
        :param element: WebDriverElement
        :return: [str] - classes found
        """
        return element.get_attribute('class').split(' ')

    def input(self, element, text, click=True, clear=True):
        '''
        Helper method to type characters into input and textarea elements. Works better with default settings than
        using just send_keys on the element.
        :param element: WebDriverElement - element to be interacted with (input, textarea)
        :param text: str - text to be written
        :param click: bool - True to click on the element before typing or clearing (prevents crashes)
        :param clear: bool - True to clear the element before typing
        :return: None
        '''
        if click:
            element.click()
        if clear:
            element.clear()
        element.send_keys(text)

    def log(self, message):
        '''
        Log function. Prints a message to console.
        :param message: str - log message
        :return: None
        '''
        print '{0} {1}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message)

    def reset_page(self):
        '''
            Resets webdriver with the same data as before.
            :return: None
        '''
        self.driver.refresh()

    def double_click(self, element):
        '''
        :return: None
        '''
        ActionChains(self.driver).double_click(element).perform()

