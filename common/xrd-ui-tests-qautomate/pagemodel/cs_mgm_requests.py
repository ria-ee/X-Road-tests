# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_mgm_requests(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160330093110
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/requests
    # Pagemodel area: (271, 1, 1647, 867)
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
    # Row count: 5
    # Element count: 20
    # Big element filter width: 55
    # Big element filter height: 40
    # Not filtered elements: button, strong, select
    # Canvas modeling: False
    # Pagemodel type: normal
    # Links found: 0
    # Page model constants:
    ID_REQUEST_DETAILS = (By.ID, u'request_details') # x: 1656 y: 8 width: 78 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_HEADING = (By.ID, u'heading') # x: 290 y: 14 width: 197 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    ID_RECORDS_COUNT = (By.ID, u'records_count') # x: 492 y: 14 width: 28 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    MANAGEMENT_REQUESTS_ALL_FILTER_TEXT = (By.CSS_SELECTOR, u'#management_requests_all_filter>label>input') # x: 346 y: 76 width: 179 height: 33, tag: input, type: text, name: None, form_id: , checkbox: , table_id: , href:
    REQUEST_ID = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 291 y: 115 width: 59 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: management_requests_all, href:
    CREATED = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[2]') # x: 350 y: 115 width: 180 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: management_requests_all, href:
    REQUEST_TYPE = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[3]') # x: 530 y: 115 width: 210 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: management_requests_all, href:
    UNKNOWN = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[4]') # x: 740 y: 115 width: 210 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: management_requests_all, href:
    SERVER_OWNER_NAME = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[5]') # x: 950 y: 115 width: 210 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: management_requests_all, href:
    SERVER_OWNER_CLASS = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[6]') # x: 1161 y: 115 width: 210 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: management_requests_all, href:
    SERVER_OWNER = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[7]') # x: 1371 y: 115 width: 210 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: management_requests_all, href:
    SERVER = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[8]') # x: 1581 y: 115 width: 210 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: management_requests_all, href:
    STATUS = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[9]') # x: 1792 y: 115 width: 107 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: management_requests_all, href:

    def click_button_id_request_details(self):
        """
        Click button to open request details
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_REQUEST_DETAILS*
        """
        # AutoGen method
        self.click_element(self.ID_REQUEST_DETAILS)

    def wait_until_element_is_visible_id_records_count(self):
        """
        Wait until records count element is visible on the page

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.ID_RECORDS_COUNT*
        """
        self.wait_until_element_is_visible(self.ID_RECORDS_COUNT)

    def search_text_from_table_management_requests_all(self, text=None):
        """
        Click management request in the management requests tab with given text
        
        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *element*
        """
        # Element search
        locator = (By.ID, u'management_requests_all')
        value =  text
        row = u'TBODY/TR'
        cell = u'TD'
        element_info = self.get_table_column_and_row_by_text(locator, value, row, cell)

        # Searched element info
        row_number = element_info[2]
        column_number = element_info[3]
        row_element = element_info[0]
        element = element_info[1]

        # Action for the element
        self.click_element(element)
