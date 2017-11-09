# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep
from common_lib.common_lib import Common_lib

class Cs_sec_servers_new_client_req_search(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    common_lib = Common_lib()
    # Pagemodel timestamp: 20151215140807
    # Pagemodel url: https://dev-cs.palveluvayla.com:4000/securityservers
    # Pagemodel area: (560, 285, 799, 399)
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
    # Links found: 2
    # Page model constants:
    UI_ACTION_MAXIMIZE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-maximize') # x: 1258 y: 285 width: 51 height: 49
    UI_ACTION_CLOSE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-close') # x: 1309 y: 285 width: 51 height: 49
    TITLE = (By.ID, u'ui-id-18') # x: 570 y: 299 width: 111 height: 21
    MEMBER_SEARCH_FILTER = (By.CSS_SELECTOR, u'#member_search_filter>label>input') # x: 631 y: 356 width: 179 height: 33
    ID_MEMBER_SEARCH_WRAPPER_NAME = (By.XPATH, u'id(\'member_search_wrapper\')/DIV[2]/DIV[1]/DIV[1]/TABLE[1]/THEAD[1]/TR[1]/TH[1]') # x: 576 y: 395 width: 128 height: 37
    MEMBER_SEARCH_WRAPPER_DATA_TABLES_SCROLL_HEAD_INNER_SORTING_ASC = (By.CSS_SELECTOR, u'#member_search_wrapper>.dataTables_scroll>.dataTables_scrollHead>.dataTables_scrollHeadInner>.dataTable>thead>tr>.sorting_asc') # x: 704 y: 395 width: 128 height: 37
    ID_MEMBER_SEARCH_WRAPPER_CLASS = (By.XPATH, u'id(\'member_search_wrapper\')/DIV[2]/DIV[1]/DIV[1]/TABLE[1]/THEAD[1]/TR[1]/TH[3]') # x: 832 y: 395 width: 128 height: 37
    ID_MEMBER_SEARCH_WRAPPER_SUBSYSTEM = (By.XPATH, u'id(\'member_search_wrapper\')/DIV[2]/DIV[1]/DIV[1]/TABLE[1]/THEAD[1]/TR[1]/TH[4]') # x: 960 y: 395 width: 128 height: 37
    CONTAINS_TEXT_INSTANCE = (By.XPATH, u'//th[contains(text(),"Instance")]') # x: 1088 y: 395 width: 128 height: 37
    CONTAINS_TEXT_TYPE = (By.XPATH, u'//th[contains(text(),"Type")]') # x: 1216 y: 395 width: 128 height: 37
    BUTTON_CANCEL = (By.CSS_SELECTOR, u'button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only') # x: 1223 y: 643 width: 77 height: 37
    BUTTON_OK = (By.ID, u'member_search_select') # x: 1310 y: 643 width: 45 height: 37

    # Dynamic objects:
    TABLECONTAINSIDMEMBER_SEARCH = (By.XPATH, u'//table[contains(@id,\'member_search\')]')     # x: 576 y: 433 width: 752 height: 671 # Dynamic object

    def click_member_from_table(self, text):
        """
        Click member in member table with parameter 'member_code'

        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_page_contains`, *text*
        """
        self.wait_until_jquery_ajax_loaded()
        self.wait_until_page_contains(text)
        element_rowtable = self.get_table_column_and_row_by_multiple_text(self.TABLECONTAINSIDMEMBER_SEARCH, text, "MEMBER","TBODY/TR","TD")
        element_rowtable[0].click()

    def click_ok_search(self):
        """
        Click button ok
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
        """
        self.click_element(self.BUTTON_OK)