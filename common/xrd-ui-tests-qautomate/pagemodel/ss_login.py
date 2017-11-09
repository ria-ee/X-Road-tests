# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_login(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20151209103101
    # Pagemodel url: https://dev-ss1.palveluvayla.com:4000/login
    # Pagemodel area: Full screen
    # Pagemodel screen resolution: (1920, 1080)
    # Use project settings: True
    # Used filters: default
    # Depth of css path: 7
    # Minimize css selector: False
    # Use css pattern: False
    # Allow non unique css pattern: False
    # Pagemodel template: False
    # Use testability: False
    # Use contains text in xpath: True
    # Exclude dynamic table filter: True
    # Row count: 25
    # Element count: 140
    # Big element filter width: 55
    # Big element filter height: 40
    # Not filtered elements: button, select, strong
    # Canvas modeling: False
    # Pagemodel type: normal
    # Links found: 0
    # Page model constants:
    LOGIN_PAGE_TITLE = (By.CSS_SELECTOR, u'h1.section-title.up.center') # x: 771 y: 396 width: 400 height: 19
    LOGIN_PAGE_SUBTITLE = (By.CSS_SELECTOR, u'h2.section-title.center') # x: 771 y: 414 width: 400 height: 16
    ID_J_USERNAME = (By.ID, u'j_username') # x: 771 y: 461 width: 400 height: 33
    ID_J_PASSWORD = (By.ID, u'j_password') # x: 771 y: 525 width: 400 height: 33
    LOGIN = (By.CLASS_NAME, u'btn') # x: 771 y: 568 width: 400 height: 33

    def login(self, parameters=None, wait_for_jquery=True):
        """
        Input text to login input fields and click button to login

        :param parameters:  Test data section dictionary
        :param wait_for_jquery:  If true method waits for jquery
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_J_USERNAME*, *parameters[u'j_username']*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_J_PASSWORD*, *parameters[u'j_password']*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.LOGIN*
            * **Step 4:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        self.input_text(self.ID_J_USERNAME, parameters[u'j_username'])
        self.input_text(self.ID_J_PASSWORD, parameters[u'j_password'])
        self.click_element(self.LOGIN)
        if wait_for_jquery:
            self.wait_until_jquery_ajax_loaded()

    def verify_contains_text(self, text=u'Authentication failed'):
        """
        Verify page contains text

        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_page_contains`, *text*
        """
        self.wait_until_page_contains(text)

    def verify_is_login_page(self):
        """
        Verify page is login page
        """
        return self.is_visible(self.ID_J_USERNAME)
