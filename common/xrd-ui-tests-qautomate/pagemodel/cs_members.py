# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from variables import errors
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class  Cs_members(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160301113247
    # Pagemodel url: https://dev-cs.palveluvayla.com:4000/#
    # Pagemodel area: (271, 3, 1645, 815)
    # Pagemodel screen resolution: (1920, 1080)
    # Use project settings: True
    # Used filters: id, css_selector, class_name, link_text, xpath
    # Xpath type: xpath-position
    # Create automated methods: True
    # Depth of css path: 4
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
    GROUP_ADD_ICON = (By.CSS_SELECTOR, u'.button-group>.add-icon') # x: 1692 y: 8 width: 54 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    MEMBER_ACTION = (By.CSS_SELECTOR, u'.member-action') # x: 1753 y: 8 width: 78 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_HEADING = (By.ID, u'heading') # x: 290 y: 14 width: 78 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    ID_RECORDS_COUNT = (By.ID, u'records_count') # x: 372 y: 14 width: 28 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    MEMBERS_ACTIONS = (By.CSS_SELECTOR, u'.members_actions') # x: 290 y: 70 width: 1610 height: 0, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href:
    DATA_TABLES_FILTER_TEXT = (By.CSS_SELECTOR, u'.dataTables_filter>label>input') # x: 346 y: 76 width: 183 height: 33, tag: input, type: text, name: None, form_id: , checkbox: , table_id: , href:
    MEMBER_NAME = (By.XPATH, u'//div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 291 y: 115 width: 814 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: members, href:
    MEMBER_CLASS = (By.XPATH, u'//div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[2]') # x: 1105 y: 115 width: 251 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: members, href:
    MEMBER = (By.XPATH, u'//div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[3]') # x: 1356 y: 115 width: 543 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: members, href:

    def click_button_group_add_icon(self):
        """
        Click button to add group icon

        **Arguments:**
            :param parameters (dict):  Test data parameters list
        
        **Steps:**
            | **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.GROUP_ADD_ICON*
        """
        # AutoGen method
        self.click_element(self.GROUP_ADD_ICON)

    def click_button_member_action(self):
        """
        Click button member actions

        **Arguments:**
            :param parameters (dict):  Test data parameters list
        
        **Steps:**
            | **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.MEMBER_ACTION*
        """
        # AutoGen method
        self.click_element(self.MEMBER_ACTION)

    def search_text_from_table_members(self, parameters=None):
        """
        Search member form members table with member name

        **Arguments:**
            :param parameters (dict):  Test data parameters list
        
        **Steps:**
            | **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_page_contains`, *parameters[u'member_name']*
        """
        # AutoGen method search_text_from_table_members
        self.wait_until_page_contains(parameters[u'member_name'])
        try:
            elem_table = self.get_table_column_and_row_by_text((By.ID, 'members'), parameters['member_name'], row='TBODY/TR', cell='TD')
            elem_table[0].click()
        except:
            elem_table = self.get_table_column_and_row_by_text_contains((By.ID, 'members'), parameters['member_name'], row='TBODY/TR', cell='TD')
            elem_table[0].click()

    def wait_until_element_is_visible_member_name(self):
        """
        Wait until page contains member name

        **Steps:**
            | **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.MEMBER_NAME*
        """
        self.wait_until_element_is_visible(self.MEMBER_NAME)

    def click_element_from_table_members(self, text=u'FirmaOy'):
        """
        Click member from members table with text

        **Arguments:**
            text(str): String value for text
        
        **Steps:**
            | **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_page_contains`, *value*
            | **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *element*
        """
        # Element search
        locator = (By.ID, 'members')
        value = text
        row = u'TBODY/TR'
        cell = u'TD'

        self.wait_until_page_contains(value)
        element_info = self.get_table_column_and_row_by_text(locator, value, row, cell)

        # Searched element info
        row_number = element_info[2]
        column_number = element_info[3] + 2
        row_element = element_info[0]
        element = row_element.find_elements(By.XPATH, cell)[int(column_number) - 1]

        # Action for the element
        self.click_element(element)

    def table_contains_member(self, text=None):
        """
        Verify table contains member with given text

        **Arguments:**
            :param parameters (dict):  Test data parameters list
        
        **Steps:**
            | **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.fail`, *errors.member_code_not_found*
        """
        locator =  (By.ID, 'members')
        if not self.table_contains_text(locator, text):
            self.fail(errors.member_code_not_found)

    def table_does_not_contain_member(self, text=None):
        """
        Verify table does not contain member with given text

        **Arguments:**
            :param parameters (dict):  Test data parameters list
        
        **Steps:**
            | **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.fail`, *errors.member_code_found*
        """
        locator =  (By.ID, 'members')
        if self.table_contains_text(locator, text):
            self.fail(errors.member_code_found)
