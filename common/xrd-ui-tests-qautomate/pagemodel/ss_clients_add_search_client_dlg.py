# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_clients_add_search_client_dlg(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160909115934
    # Pagemodel url: https://test-ss2.i.palveluvayla.com:4000/clients
    # Pagemodel area: (625, 234, 674, 506)
    # Pagemodel screen resolution: (1920, 1080)
    # Use project settings: True
    # Used filters: id, css_selector, class_name, link_text, xpath
    # Xpath type: xpath-position
    # Create automated methods: True
    # Depth of css path: 3
    # Minimize css selector: True
    # Use css pattern: False
    # Allow non unique css pattern: False
    # Pagemodel template: False
    # Use testability: True
    # testability attribute: data-name
    # Use contains text in xpath: True
    # Exclude dynamic table filter: True
    # Row count: 2
    # Element count: 10
    # Big element filter width: 55
    # Big element filter height: 40
    # Not filtered elements: button, strong, select
    # Canvas modeling: False
    # Pagemodel type: normal
    # Links found: 0
    # Page model constants:
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[8]/div[1]/div[1]/button[1]') # x: 1191 y: 236 width: 51 height: 49, tag: button, type: submit, name: None, form_id: clients, checkbox: , table_id: clients_global, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[8]/div[1]/div[1]/button[2]') # x: 1242 y: 236 width: 51 height: 49, tag: button, type: submit, name: None, form_id: clients, checkbox: , table_id: clients_global, href:
    TITLE = (By.ID, u'ui-id-12') # x: 637 y: 250 width: 87 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    NAME_SEARCH_MEMBER_TEXT = (By.CSS_SELECTOR, u'input[name="search_member"]') # x: 642 y: 301 width: 179 height: 33, tag: input, type: text, name: search_member, form_id: clients, checkbox: , table_id: , href:
    SIMPLE_SEARCH = (By.CSS_SELECTOR, u'.simple_search_form>.search') # x: 824 y: 301 width: 78 height: 33, tag: button, type: submit, name: None, form_id: clients, checkbox: , table_id: , href:
    SIMPLE_SEARCH_SHOW_ONLY_LOCAL_CLIENTS = (By.CSS_SELECTOR, u'.simple_search_form>label') # x: 906 y: 307 width: 157 height: 21, tag: label, type: , name: None, form_id: clients, checkbox: , table_id: , href:
    ID_SEARCH_FILTER = (By.ID, u'search_filter') # x: 1062 y: 310 width: 13 height: 13, tag: input, type: checkbox, name: search_filter, form_id: clients, checkbox: , table_id: , href:
    MEMBER_NAME = (By.XPATH, u'//div[8]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 643 y: 350 width: 264 height: 37, tag: th, type: , name: None, form_id: clients, checkbox: , table_id: clients_global, href:
    MEMBER_CLASS = (By.XPATH, u'//div[8]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[2]') # x: 907 y: 350 width: 105 height: 37, tag: th, type: , name: None, form_id: clients, checkbox: , table_id: clients_global, href:
    MEMBER = (By.XPATH, u'//div[8]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[3]') # x: 1012 y: 350 width: 133 height: 37, tag: th, type: , name: None, form_id: clients, checkbox: , table_id: clients_global, href:
    SUBSYSTEM = (By.XPATH, u'//div[2]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[4]') # x: 1145 y: 350 width: 133 height: 37, tag: th, type: , name: None, form_id: clients, checkbox: , table_id: clients_global, href:
    NO_MATCHING_RECORDS = (By.XPATH, u'//div[8]/div[2]/div[1]/div[2]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[1]') # x: 643 y: 388 width: 635 height: 31, tag: td, type: , name: None, form_id: clients, checkbox: , table_id: clients_global, href:
    BUTTON_CANCEL = (By.XPATH, u'//div[8]/div[3]/div[1]/button[2]') # x: 1156 y: 694 width: 77 height: 37, tag: button, type: button, name: cancel, form_id: clients, checkbox: , table_id: clients_global, href:
    BUTTON_OK = (By.ID, u'client_select_ok') # x: 1243 y: 694 width: 45 height: 37, tag: button, type: button, name: ok, form_id: , checkbox: , table_id: , href:

    def click_button_id_client_select(self):
        """
        Click button to select

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_CLIENT_SELECT*
        """
        # AutoGen method
        self.click_element(self.ID_CLIENT_SELECT)

    def click_button_id_client_select_ok(self):
        """
        Click button to ok
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
        """
        # AutoGen method
        self.click_element(self.BUTTON_OK)

    def click_client_from_table_clientsglobal(self, parameters=None):
        """
        Click client from clients table with parameter 'subsystem_code'
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_page_contains`, *parameters[u'subsystem_code']*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *table_element[0]*
        """
        # AutoGen method search_text_from_table_clientsglobal
        self.wait_until_page_contains(parameters[u'subsystem_code'])
        table_element = self.get_table_column_and_row_by_text((By.ID, 'clients_global'), parameters['subsystem_code'], row='TBODY/TR', cell='TD')
        self.click_element(table_element[0]) # Click table row which contains search text

    def click_element_id_search_filter(self):
        """
        Click button to filter

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_SEARCH_FILTER*
        """
        self.click_element(self.ID_SEARCH_FILTER)
