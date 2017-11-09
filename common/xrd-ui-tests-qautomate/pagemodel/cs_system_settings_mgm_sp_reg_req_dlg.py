# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_system_settings_mgm_sp_reg_req_dlg(CommonUtils):
    """

    """
    # Pagemodel timestamp: 20161011132454
    # Pagemodel url: https://test-cs2.i.palveluvayla.com:4000/system_settings
    # Pagemodel area: (680, 188, 563, 598)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[9]/div[1]/div[1]/button[1]') # x: 1138 y: 188 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 6, href: 
    MENUBAR_CLOSE = (By.XPATH, u'//div[9]/div[1]/div[1]/button[2]') # x: 1189 y: 188 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 6, href: 
    TITLE = (By.ID, u'ui-id-5') # x: 690 y: 203 width: 363 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    CLIENT_INFORMATION = (By.XPATH, u'//section[1]/h2[1]/span[1]') # x: 705 y: 261 width: 165 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: 6, href: None
    NAME = (By.XPATH, u'//section[1]/table[1]/tbody[1]/tr[1]/td[1]') # x: 705 y: 290 width: 130 height: 43, tag: td, type: , name: None, form_id: , checkbox: , table_id: 6, href: 
    ID_USED_SERVER_NAME = (By.ID, u'used_server_name') # x: 840 y: 295 width: 373 height: 33, tag: p, type: , name: None, form_id: , checkbox: , table_id: 5, href: 
    CLASS = (By.XPATH, u'//section[1]/table[1]/tbody[1]/tr[2]/td[1]') # x: 705 y: 333 width: 130 height: 43, tag: td, type: , name: None, form_id: , checkbox: , table_id: 6, href: 
    ID_USED_SERVER_CLASS = (By.ID, u'used_server_class') # x: 840 y: 338 width: 373 height: 33, tag: p, type: , name: None, form_id: , checkbox: , table_id: 5, href: 
    UNKNOWN_0 = (By.XPATH, u'//section[1]/table[1]/tbody[1]/tr[3]/td[1]') # x: 705 y: 376 width: 130 height: 43, tag: td, type: , name: None, form_id: , checkbox: , table_id: 6, href: 
    ID_USED_SERVER_CODE = (By.ID, u'used_server_code') # x: 840 y: 381 width: 373 height: 33, tag: p, type: , name: None, form_id: , checkbox: , table_id: 5, href: 
    SUBSYSTEM = (By.XPATH, u'//section[1]/table[1]/tbody[1]/tr[4]/td[1]') # x: 705 y: 419 width: 130 height: 43, tag: td, type: , name: None, form_id: , checkbox: , table_id: 6, href: 
    ID_USED_SERVER_SUBSYSTEM_CODE = (By.ID, u'used_server_subsystem_code') # x: 840 y: 424 width: 373 height: 33, tag: input, type: text, name: None, form_id: , checkbox: , table_id: 5, href: 
    SECURITY_SERVER_INFORMATION = (By.XPATH, u'//section[2]/h2[1]/span[1]') # x: 705 y: 479 width: 244 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: 6, href: None
    ID_USED_SERVER_SERVER_SEARCH = (By.ID, u'used_server_server_search') # x: 710 y: 513 width: 78 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 6, href: 
    OWNER_NAME = (By.XPATH, u'//section[2]/table[1]/tbody[1]/tr[2]/td[1]') # x: 705 y: 551 width: 130 height: 42, tag: td, type: , name: None, form_id: , checkbox: , table_id: 6, href: 
    ID_USED_SERVER_OWNER_NAME = (By.ID, u'used_server_owner_name') # x: 840 y: 556 width: 373 height: 32, tag: p, type: , name: None, form_id: , checkbox: , table_id: 6, href: 
    OWNER_CLASS = (By.XPATH, u'//section[2]/table[1]/tbody[1]/tr[3]/td[1]') # x: 705 y: 593 width: 130 height: 42, tag: td, type: , name: None, form_id: , checkbox: , table_id: 6, href: 
    ID_USED_SERVER_OWNER_CLASS = (By.ID, u'used_server_owner_class') # x: 840 y: 598 width: 373 height: 32, tag: p, type: , name: None, form_id: , checkbox: , table_id: 6, href: 
    OWNER = (By.XPATH, u'//section[2]/table[1]/tbody[1]/tr[4]/td[1]') # x: 705 y: 635 width: 130 height: 42, tag: td, type: , name: None, form_id: , checkbox: , table_id: 6, href: 
    ID_USED_SERVER_OWNER_CODE = (By.ID, u'used_server_owner_code') # x: 840 y: 640 width: 373 height: 32, tag: p, type: , name: None, form_id: , checkbox: , table_id: 6, href: 
    SERVER = (By.XPATH, u'//section[2]/table[1]/tbody[1]/tr[5]/td[1]') # x: 705 y: 677 width: 130 height: 42, tag: td, type: , name: None, form_id: , checkbox: , table_id: 6, href: 
    ID_USED_SERVER_SERVER_CODE = (By.ID, u'used_server_server_code') # x: 840 y: 682 width: 373 height: 32, tag: p, type: , name: None, form_id: , checkbox: , table_id: 6, href: 

    # Dynamic objects:
    BUTTON_SUBMIT = (By.XPATH, u'//button[contains(@id,\'member_used_server_register_submit\')]')  # x: 1159 y: 745 width: 76 height: 37 # Dynamic object

    def click_button_id_used_server_server_search(self):
        """
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_USED_SERVER_SERVER_SEARCH*
        """
        # AutoGen method
        self.click_element(self.ID_USED_SERVER_SERVER_SEARCH)

    def click_button_submit(self):
        """
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_SUBMIT*
        """
        self.click_element(self.BUTTON_SUBMIT)
