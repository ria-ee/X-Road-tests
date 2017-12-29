# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_system_settings_search_member(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20161010132204
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/system_settings
    # Pagemodel area: (558, 286, 803, 401)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[9]/div[1]/div[1]/button[1]') # x: 1258 y: 286 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: member_search, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[9]/div[1]/div[1]/button[2]') # x: 1309 y: 286 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: member_search, href:
    TITLE = (By.ID, u'ui-id-5') # x: 570 y: 300 width: 111 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    DATA_TABLES_FILTER_TEXT = (By.CSS_SELECTOR, u'.dataTables_filter>label>input') # x: 631 y: 357 width: 179 height: 33, tag: input, type: text, name: None, form_id: , checkbox: , table_id: , href:
    NAME = (By.XPATH, u'//div[2]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 576 y: 396 width: 128 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: member_search, href:
    CLASS = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[3]') # x: 832 y: 396 width: 128 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: member_search, href:
    INSTANCE = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[5]') # x: 1088 y: 396 width: 128 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: member_search, href:
    TYPE = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[6]') # x: 1216 y: 396 width: 128 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: member_search, href:
    BUTTON_CANCEL = (By.XPATH, u'//div[9]/div[3]/div[1]/button[2]') # x: 1197 y: 644 width: 77 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: member_search, href:

    # Dynamic objects:
    BUTTON_SELECT = (By.XPATH, u'//div[9]/div[3]/div[1]/button[1]') # x: 1284 y: 644 width: 71 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: , href: # Dynamic object

    def click_member_from_table_membersearch(self, parameters=None):
        """
        Click member from members table with parameter 'member_name'

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_page_contains`, *parameters[u'member_name']*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *table_element[0]*
        """
        self.wait_until_page_contains(parameters[u'member_name'])
        table_element = self.get_table_column_and_row_by_text_contains((By.ID, 'member_search'), parameters['member_name'], row='TBODY/TR', cell='TD')
        self.click_element(table_element[0]) # Click table row which contains search text

    def wait_until_element_is_visible_type(self):
        """
        Wait until type element is visible on the page

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.TYPE*
        """
        self.wait_until_element_is_visible(self.TYPE)

    def click_element_dlg_select(self):
        """
        Click element to select member

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_SELECT*
        """
        self.click_element(self.BUTTON_SELECT)
