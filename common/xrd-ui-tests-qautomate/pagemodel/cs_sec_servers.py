# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from variables import errors
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_sec_servers(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20151215121320
    # Pagemodel url: https://dev-cs.palveluvayla.com:4000/securityservers
    # Pagemodel area: (271, 2, 1647, 653)
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
    ID_SECURITYSERVER_EDIT = (By.ID, u'securityserver_edit')  # x: 1752 y: 8 width: 78 height: 33
    ID_HEADING = (By.ID, u'heading') # x: 290 y: 14 width: 143 height: 22
    ID_RECORDS_COUNT = (By.ID, u'records_count') # x: 438 y: 14 width: 28 height: 22
    SECURITYSERVERS_ACTIONS = (By.CSS_SELECTOR, u'.securityservers_actions') # x: 290 y: 70 width: 1610 height: 0
    SECURITYSERVERS_FILTER = (By.CSS_SELECTOR, u'#securityservers_filter>label>input') # x: 346 y: 76 width: 179 height: 33
    DATA_TABLES_SCROLL_HEAD_INNER_SECURITYSERVER_SERVER = (By.CSS_SELECTOR, u'.dataTables_scrollHeadInner>.dataTable>thead>tr>#securityserver_server_code') # x: 291 y: 115 width: 332 height: 37
    DATA_TABLES_SCROLL_HEAD_INNER_SECURITYSERVER_OWNER_NAME = (By.CSS_SELECTOR, u'.dataTables_scrollHeadInner>.dataTable>thead>tr>#securityserver_owner_name') # x: 623 y: 115 width: 613 height: 37
    DATA_TABLES_SCROLL_HEAD_INNER_SECURITYSERVER_OWNER_CLASS = (By.CSS_SELECTOR, u'.dataTables_scrollHeadInner>.dataTable>thead>tr>#securityserver_owner_class') # x: 1236 y: 115 width: 251 height: 37
    DATA_TABLES_SCROLL_HEAD_INNER_SECURITYSERVER_OWNER = (By.CSS_SELECTOR, u'.dataTables_scrollHeadInner>.dataTable>thead>tr>#securityserver_owner_code') # x: 1487 y: 115 width: 412 height: 37
    ID_SECURITYSERVERS = (By.ID, u'securityservers') # x: 291 y: 153 width: 1608 height: 383

    # Dynamic objects:

    def click_ss_details(self):
        """
        Click button to show security server details dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_SECURITYSERVER_EDIT*
        """
        self.click_element(self.ID_SECURITYSERVER_EDIT)

    def click_security_servers_row_with_text(self, text=u'FirmaOy'):
        """
        Click security server in security servers table with given text
        
        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_page_contains`, *text*
        """
        self.wait_until_jquery_ajax_loaded()
        self.wait_until_page_contains(text)
        element_rowtable = self.get_table_column_and_row_by_text(self.ID_SECURITYSERVERS, text,"TBODY/TR","TD")
        element_rowtable[0].click()

    def table_contains_server(self, text=None):
        """
        Verify security servers table contains server with given text

        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.fail`, *errors.member_code_not_found*
        """
        self.wait_until_jquery_ajax_loaded()
        if not self.table_contains_text(self.ID_SECURITYSERVERS, text):
           self.fail(errors.member_code_not_found)

    def table_does_not_contain_server(self, text=None):
        """
        Verify security servers table does not contain server with given text
        
        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.fail`, *errors.member_code_found*
        """
        self.wait_until_jquery_ajax_loaded()
        if self.table_contains_text(self.ID_SECURITYSERVERS, text):
           self.fail(errors.member_code_found)
