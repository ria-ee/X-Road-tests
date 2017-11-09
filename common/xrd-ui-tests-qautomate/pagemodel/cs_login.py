# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_login(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20151211094223
    # Pagemodel url: https://dev-cs.palveluvayla.com:4000/login
    # Pagemodel area: Full screen
    # Pagemodel screen resolution: (1920, 1080)
    # Use project settings: True
    # Used filters: id, css_selector, class_name, link_text, xpath
    # Depth of css path: 8
    # Minimize css selector: True
    # Use css pattern: False
    # Allow non unique css pattern: False
    # Pagemodel template: False
    # Use testability: True
    # testability attribute: data-name
    # Use contains text in xpath: True
    # Exclude dynamic table filter: True
    # Row count: 5
    # Element count: 20
    # Big element filter width: 55
    # Big element filter height: 40
    # Not filtered elements: button, strong, select
    # Canvas modeling: False
    # Pagemodel type: normal
    # Links found: 0
    # Page model constants:
    TITLE = (By.CSS_SELECTOR, u'h1.section-title.up.center') # x: 771 y: 396 width: 400 height: 19
    SUBTITLE = (By.CSS_SELECTOR, u'h2.section-title.center') # x: 771 y: 414 width: 400 height: 16
    TEXT_USERNAME = (By.CSS_SELECTOR, u'span.text') # x: 771 y: 440 width: 78 height: 21
    ID_J_USERNAME = (By.ID, u'j_username') # x: 771 y: 461 width: 400 height: 33
    ID_J_PASSWORD = (By.ID, u'j_password') # x: 771 y: 525 width: 400 height: 33
    BTN_LOGIN = (By.CSS_SELECTOR, u'.btn') # x: 771 y: 568 width: 400 height: 33

    def login_dev_cs(self, parameters=None):
        """
        Login to central server

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_J_USERNAME*, *parameters[u'j_username']*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_J_PASSWORD*, *parameters[u'j_password']*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BTN_LOGIN*
            * **Step 4:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # AutoGen method submit form: login
        self.input_text(self.ID_J_USERNAME, parameters[u'j_username'])
        self.input_text(self.ID_J_PASSWORD, parameters[u'j_password'])
        self.click_element(self.BTN_LOGIN)
        self.wait_until_jquery_ajax_loaded()

    def verify_is_login_page(self, parameters=None):
        """
        Verify page is login page
        :param parameters:  Test data section dictionary
        """
        return self.is_visible(self.ID_J_USERNAME)
