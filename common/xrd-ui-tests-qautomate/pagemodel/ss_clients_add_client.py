# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_clients_add_client(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20151214092407
    # Pagemodel url: https://dev-ss1.palveluvayla.com:4000/clients
    # Pagemodel area: (774, 305, 371, 363)
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
    UI_ACTION_MAXIMIZE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-maximize') # x: 1043 y: 304 width: 51 height: 49
    UI_ACTION_CLOSE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-close') # x: 1094 y: 304 width: 51 height: 49
    TITLE = (By.ID, u'ui-id-11') # x: 785 y: 318 width: 73 height: 21
    ID_CLIENT_SELECT = (By.ID, u'client_select') # x: 828 y: 379 width: 265 height: 33
    ID_ADD_MEMBER_NAME = (By.ID, u'add_member_name') # x: 927 y: 440 width: 194 height: 31
    ID_ADD_MEMBER_CLASS = (By.ID, u'add_member_class') # x: 932 y: 476 width: 185 height: 35
    ID_ADD_MEMBER_CODE = (By.ID, u'add_member_code') # x: 932 y: 521 width: 186 height: 33
    ID_ADD_SUBSYSTEM_CODE = (By.ID, u'add_subsystem_code') # x: 932 y: 564 width: 186 height: 33
    DATA_NAME_CANCEL = (By.CSS_SELECTOR, u'button[data-name="cancel"]') # x: 1008 y: 624 width: 77 height: 37

    # Dynamic objects:
    CONTAINSDATANAMEOK3 = (By.XPATH, u'(//*[contains(@data-name,\'ok\')])[3]')     # x: 1096 y: 622 width: 44 height: 37 # Dynamic object
    BUTTON_OK = (By.XPATH, u'//div[7]/div[3]/div[1]/button[1]') # x: 1095 y: 625 width: 45 height: 37, tag: button, type: button, name: ok, form_id: , checkbox: , table_id: , href: # Dynamic object

    def fill_and_submit_client_details(self, parameters=None):
        """
        Fill fields for generating new client. Paramters used are 'member_code', 'subsystem_code' and 'member_class'

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_ADD_MEMBER_CODE*, *parameters[u'member_code']*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_ADD_SUBSYSTEM_CODE*, *parameters[u'subsystem_code']*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.select_from_list_by_label`, *self.ID_ADD_MEMBER_CLASS*, *parameters[u'member_class']*
            * **Step 4:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.CONTAINSDATANAMEOK3*
            * **Step 5:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # TODO FIX
        self.input_text(self.ID_ADD_MEMBER_CODE, parameters[u'member_code'])
        self.input_text(self.ID_ADD_SUBSYSTEM_CODE, parameters[u'subsystem_code'])
        self.select_from_list_by_label(self.ID_ADD_MEMBER_CLASS, parameters[u'member_class'])
        self.click_element(self.CONTAINSDATANAMEOK3)
        self.wait_until_jquery_ajax_loaded()
        sleep(5)

    def cancel_client_adding(self):
        """
        Click button to cancel the client generation
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DATA_NAME_CANCEL*
        """
        if self.is_visible(self.DATA_NAME_CANCEL, 5):
            self.click_element(self.DATA_NAME_CANCEL)

    def click_element_id_client_select(self):
        """
        Click button to select

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_CLIENT_SELECT*
        """
        self.click_element(self.ID_CLIENT_SELECT)

    def click_element_ok(self):
        """
        Click element to ok

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
        """
        # TODO FIX
        self.click_element(self.BUTTON_OK)
