# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_system_settings_mgm_req_servers_dlg(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20161011132706
    # Pagemodel url: https://test-cs2.i.palveluvayla.com:4000/system_settings
    # Pagemodel area: (531, 269, 859, 433)
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
    # Row count: 7
    # Element count: 30
    # Big element filter width: 55
    # Big element filter height: 40
    # Not filtered elements: button, strong, select
    # Canvas modeling: False
    # Pagemodel type: normal
    # Links found: 0
    # Page model constants:
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[8]/div[1]/div[1]/button[1]') # x: 1288 y: 271 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 8, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[8]/div[1]/div[1]/button[2]') # x: 1339 y: 271 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 8, href:
    TITLE = (By.ID, u'ui-id-4') # x: 540 y: 285 width: 114 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    USED_SERVER_SEARCH_ALL_FILTER_TEXT = (By.CSS_SELECTOR, u'#used_server_search_all_filter>label>input') # x: 611 y: 352 width: 179 height: 33, tag: input, type: text, name: None, form_id: , checkbox: , table_id: , href:
    OWNER_NAME_0 = (By.XPATH, u'//div[2]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 556 y: 391 width: 202 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: 8, href:
    OWNER_CLASS_0 = (By.XPATH, u'//div[2]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[2]') # x: 758 y: 391 width: 202 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: 8, href:
    OWNER_0 = (By.XPATH, u'//div[1]/div[1]/table[1]/thead[1]/tr[1]/th[3]') # x: 960 y: 391 width: 202 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: 8, href:
    SERVER = (By.XPATH, u'//div[1]/div[1]/table[1]/thead[1]/tr[1]/th[4]') # x: 1162 y: 391 width: 202 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: 8, href:
    BUTTON_CANCEL = (By.XPATH, u'//div[8]/div[3]/div[1]/button[2]') # x: 1227 y: 659 width: 77 height: 37, tag: button, type: button, name: cancel, form_id: , checkbox: , table_id: 8, href:

    # Dynamic objects:
    BUTTON_SELECT = (By.XPATH, u'//button[contains(@id,\'member_securityserver_search_select\')]')  # x: 1314 y: 659 width: 71 height: 37 # Dynamic object

    def click_server_from_table_usedserversearchall(self, parameters=None):
        """
        Click used server in used servers table with parameter 'member_name'.

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_page_contains`, *parameters[u'member_name']*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *table_element[0]*
        """
        self.wait_until_jquery_ajax_loaded()
        self.wait_until_page_contains(parameters[u'member_name'])
        table_element = self.get_table_column_and_row_by_text_contains((By.ID, 'used_server_search_all'), parameters['member_name'], row='TBODY/TR', cell='TD')
        self.click_element(table_element[0]) # Click table row which contains search text

    def click_button_select(self):
        """
        Click button to select used server

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_SELECT*
        """
        self.click_element(self.BUTTON_SELECT)
