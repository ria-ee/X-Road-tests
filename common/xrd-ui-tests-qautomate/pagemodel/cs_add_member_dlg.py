# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_add_member_dlg(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20161010120102
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/
    # Pagemodel area: (708, 308, 504, 355)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[1]') # x: 1108 y: 311 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: member_add_table, href:
    TITLE = (By.ID, u'ui-id-7') # x: 720 y: 325 width: 92 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    MEMBER_NAME = (By.XPATH, u'//div[2]/div[1]/section[1]/form[1]/table[1]/tbody[1]/tr[1]/td[1]') # x: 735 y: 386 width: 111 height: 43, tag: td, type: , name: None, form_id: , checkbox: , table_id: member_add_table, href:
    TEXT_0 = (By.XPATH, u'//section[1]/form[1]/table[1]/tbody[1]/tr[1]/td[2]/input[1]') # x: 851 y: 391 width: 332 height: 33, tag: input, type: text, name: None, form_id: , checkbox: , table_id: member_add_table, href:
    MEMBER_CLASS = (By.XPATH, u'//div[2]/div[1]/section[1]/form[1]/table[1]/tbody[1]/tr[2]/td[1]') # x: 735 y: 429 width: 111 height: 45, tag: td, type: , name: None, form_id: , checkbox: , table_id: member_add_table, href:
    NAME_MEMBER_ADD_CLASS_DETAIL_GOV = (By.CSS_SELECTOR, u'select[name="member_add_class"].detail_input') # x: 851 y: 434 width: 331 height: 35, tag: select, type: , name: member_add_class, form_id: , checkbox: , table_id: member_add_table, href:
    MEMBER = (By.XPATH, u'//div[2]/div[1]/section[1]/form[1]/table[1]/tbody[1]/tr[3]/td[1]') # x: 735 y: 474 width: 111 height: 43, tag: td, type: , name: None, form_id: , checkbox: , table_id: member_add_table, href:
    TEXT = (By.XPATH, u'//tr[3]/td[2]/input[1]') # x: 851 y: 479 width: 332 height: 33, tag: input, type: text, name: None, form_id: , checkbox: , table_id: member_add_table, href:
    BUTTON_CANCEL = (By.XPATH, u'//div[7]/div[3]/div[1]/button[2]') # x: 1073 y: 619 width: 77 height: 37, tag: button, type: button, name: cancel, form_id: , checkbox: , table_id: member_add_table, href:
    BUTTON_OK = (By.XPATH, u'//div[7]/div[3]/div[1]/button[1]') # x: 1160 y: 619 width: 45 height: 37, tag: button, type: button, name: ok, form_id: , checkbox: , table_id: member_add_table, href:

    def click_button_ok_0(self):
        """
        Click ok button

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
        """
        # AutoGen method
        self.click_element(self.BUTTON_OK)

    def fill_input_add_member(self, parameters=None):
        """
        Fill member values to add member
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.TEXT_0*, *parameters['member_name']*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.select_from_list_by_label`, *self.NAME_MEMBER_ADD_CLASS_DETAIL_GOV*, *parameters['member_class']*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.TEXT*, *parameters['member_code']*
        """
        self.input_text(self.TEXT_0, parameters['member_name'])
        self.select_from_list_by_label(self.NAME_MEMBER_ADD_CLASS_DETAIL_GOV, parameters['member_class'])
        self.input_text(self.TEXT, parameters['member_code'])
