# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_conf_mgm_internal_new_key(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20161101080519
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/configuration_management
    # Pagemodel area: (708, 385, 504, 204)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[1]') # x: 1108 y: 386 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 5, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[2]') # x: 1159 y: 386 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 5, href:
    TITLE = (By.ID, u'ui-id-6') # x: 720 y: 400 width: 61 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    TOKEN = (By.XPATH, u'//div[7]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[1]') # x: 725 y: 451 width: 54 height: 45, tag: td, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    ID_TOKEN_ID = (By.ID, u'token_id') # x: 784 y: 456 width: 408 height: 35, tag: select, type: , name: token_id, form_id: , checkbox: , table_id: 5, href:
    ID_LABEL = (By.ID, u'label') # x: 784 y: 501 width: 408 height: 33, tag: input, type: text, name: label, form_id: , checkbox: , table_id: 5, href:
    BUTTON_OK = (By.XPATH, u'//div[7]/div[3]/div[1]/button[1]') # x: 1160 y: 544 width: 45 height: 37, tag: button, type: button, name: ok, form_id: , checkbox: , table_id: 5, href:

    def click_button_ok(self):
        """
        Click button to ok the dialog
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # AutoGen method
        self.click_element(self.BUTTON_OK)
        self.wait_until_jquery_ajax_loaded()
