# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = self.get_current_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Common_elements(CommonUtils):
    """
Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20170521232724
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/
    # Pagemodel area: (5, 1, 1891, 69)
    # Pagemodel screen resolution: (3840, 1080)
    # Use project settings: True
    # Used filters: id, css_selector, class_name, link_text, xpath
    # Xpath type: xpath-position
    # Create automated methods: False
    # Depth of css path: 3
    # Minimize css selector: True
    # Use css pattern: False
    # Allow non unique css pattern: False
    # Pagemodel template: False
    # Use testability: True
    # testability attribute: data-name
    # Use contains text in xpath: False
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

    # Dynamic objects:
    MESSAGE = (By.CLASS_NAME, u'message') # x: 270 y: 956 width: 1650 height: 28, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href:
    LOG_OUT = (By.LINK_TEXT, u'log out') # x: 1755 y: 153 width: 165 height: 30, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://xroad-lxd-cs.lxd:4000/login/logout
    LANGUAGE_CHANGE = (By.ID, u'locale_select') # x: 1755 y: 122 width: 165 height: 30, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://xroad-lxd-cs.lxd:4000/#
    USER_INFO = (By.ID, u'user-info') # x: 1757 y: 71 width: 163 height: 51, tag: li, type: , name: None, form_id: , checkbox: , table_id: , href:
    ALERT_MESSAGE = (By.ID, u'alerts') # x: 0 y: 0 width: 1920 height: 71, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href:

    def verify_message_contains(self, message=u'Internal configuration anchor generated successfully'):
        """
        Verify bottom message text

        :param message:  String value for message
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_should_contain`, *self.MESSAGE*, *message*
        """
        self.element_should_contain(self.MESSAGE, message)

    def click_user_info(self):
        """
        Click user info menu button

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.mouse_over`, *self.USER_INFO*
        """
        self.mouse_over(self.USER_INFO)

    def click_log_out(self):
        """
        Click log out from user info menu

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.LOG_OUT*
        """
        self.click_element(self.LOG_OUT)

    def click_change_language(self):
        """

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.LANGUAGE_CHANGE*
        """
        self.click_element(self.LANGUAGE_CHANGE)
