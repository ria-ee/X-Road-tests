# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = self.get_current_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Dlg_change_language(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20170509100502
    # Pagemodel url: https://xroad-lxd-ss2.lxd:4000/clients#
    # Pagemodel area: (834, 403, 254, 153)
    # Pagemodel screen resolution: (1920, 1080)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[5]/div[1]/div[1]/button[1]') # x: 983 y: 404 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: clients, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[5]/div[1]/div[1]/button[2]') # x: 1034 y: 404 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: clients, href:
    TITLE = (By.ID, u'ui-id-2') # x: 845 y: 418 width: 118 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    ID_LOCALE = (By.XPATH, u'//select[@id="locale"]/option') # x: 901 y: 469 width: 119 height: 34, tag: select, type: , name: locale, form_id: , checkbox: , table_id: , href:
    BUTTON_CANCEL = (By.XPATH, u'//div[5]/div[3]/div[1]/button[2]') # x: 951 y: 516 width: 75 height: 36, tag: button, type: button, name: cancel, form_id: , checkbox: , table_id: clients, href:
    BUTTON_OK = (By.XPATH, u'//div[5]/div[3]/div[1]/button[1]') # x: 1036 y: 516 width: 44 height: 36, tag: button, type: button, name: ok, form_id: , checkbox: , table_id: clients, href:

    def click_button_ok(self):
        """
        Click button to ok the dialog
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
        """
        self.click_element(self.BUTTON_OK)

    def change_language(self, text=None):
        """
        
        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *element*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.fail`, *"Option not found"*
        """
        #TODO improve
        locator = self.ID_LOCALE
        elements = self.find_elements(locator)
        for element in elements:
            if element.text == text:
                self.click_element(element)
                return
        self.fail("Option not found")

    def click_button_cancel(self):
        """
        Click button to cancel the dialog
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_CANCEL*
        """
        self.click_element(self.BUTTON_CANCEL)
