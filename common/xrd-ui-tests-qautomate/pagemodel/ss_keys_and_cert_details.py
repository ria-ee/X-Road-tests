# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = self.get_current_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_keys_and_cert_details(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20170417111134
    # Pagemodel url: https://xroad-lxd-ss2.lxd:4000/keys
    # Pagemodel area: (612, 180, 695, 602)
    # Pagemodel screen resolution: (1920, 1080)
    # Use project settings: True
    # Used filters: id, css_selector, class_name, link_text, xpath
    # Xpath type: xpath-position
    # Create automated methods: False
    # Depth of css path: 3
    # Minimize css selector: True
    # Use css pattern: False
    # Allow non unique css pattern: False
    # Pagemodel template: False
    # Use testability: True
    # testability attribute: data-name
    # Use contains text in xpath: False
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[12]/div[1]/div[1]/button[1]') # x: 1208 y: 180 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: keys, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[12]/div[1]/div[1]/button[2]') # x: 1259 y: 180 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: keys, href:
    TITLE = (By.ID, u'ui-id-8') # x: 620 y: 195 width: 130 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    HASH_SHA_1 = (By.CSS_SELECTOR, u'h3>span') # x: 635 y: 647 width: 107 height: 23, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    ID_HASH = (By.ID, u'hash') # x: 635 y: 681 width: 641 height: 38, tag: pre, type: , name: None, form_id: , checkbox: , table_id: , href:
    BUTTON_OK = (By.XPATH, u'//div[12]/div[3]/div[1]/button[1]') # x: 1261 y: 739 width: 44 height: 36, tag: button, type: button, name: ok, form_id: , checkbox: , table_id: keys, href:

    def verify_hash(self):
        """
        Verify that hash is present on page
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_should_be_present`, *self.ID_HASH*
        """
        self.element_should_be_present(self.ID_HASH)
