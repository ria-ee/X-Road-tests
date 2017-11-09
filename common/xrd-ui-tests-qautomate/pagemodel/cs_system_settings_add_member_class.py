# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_system_settings_add_member_class(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20161007091041
    # Pagemodel url: https://test-cs2.i.palveluvayla.com:4000/system_settings
    # Pagemodel area: (710, 363, 503, 248)
    # Pagemodel screen resolution: (1920, 1080)
    # Use project settings: True
    # Used filters: id, css_selector, class_name, link_text, xpath
    # Xpath type: xpath-position
    # Depth of css path: 3
    # Minimize css selector: True
    # Create automated methods: True
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[9]/div[1]/div[1]/button[1]') # x: 1108 y: 364 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 5, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[9]/div[1]/div[1]/button[2]') # x: 1159 y: 364 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 5, href:
    TITLE = (By.ID, u'ui-id-5') # x: 720 y: 378 width: 132 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    NAME_MEMBER_CLASS_FILL_TEXT = (By.CSS_SELECTOR, u'input[name="member_class_code"].fill') # x: 871 y: 434 width: 321 height: 33, tag: input, type: text, name: member_class_code, form_id: , checkbox: , table_id: 5, href:
    DESCRIPTION = (By.XPATH, u'//div[2]/div[1]/table[1]/tbody[1]/tr[2]/td[1]') # x: 725 y: 472 width: 141 height: 81, tag: td, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    NAME_MEMBER_CLASS_DESCRIPTION = (By.CSS_SELECTOR, u'textarea[name="member_class_description"]') # x: 871 y: 477 width: 321 height: 71, tag: textarea, type: , name: member_class_description, form_id: , checkbox: , table_id: 5, href:
    BUTTON_CANCEL = (By.XPATH, u'//div[9]/div[3]/div[1]/button[2]') # x: 1073 y: 566 width: 77 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: 5, href:
    BUTTON_OK = (By.XPATH, u'//div[9]/div[3]/div[1]/button[1]') # x: 1160 y: 566 width: 45 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: 5, href:

    def input_text_to_name_member_class_fill_text(self, parameters=None):
        """
        Input text to member name field. Parameter used is 'member_class'
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.NAME_MEMBER_CLASS_FILL_TEXT*, *parameters['member_class']*
        """
        # AutoGen method
        self.input_text(self.NAME_MEMBER_CLASS_FILL_TEXT, parameters['member_class'])

    def click_button_ok(self):
        """
        Click button to ok the dialog
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
        """
        # AutoGen method
        self.click_element(self.BUTTON_OK)

    def input_text_name_member_class_description(self, parameters=None):
        """
        Input text to member description field. Parameter used is 'member_class_description'
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.NAME_MEMBER_CLASS_DESCRIPTION*, *parameters[u'member_class_description']*
        """
        self.input_text(self.NAME_MEMBER_CLASS_DESCRIPTION, parameters[u'member_class_description'])