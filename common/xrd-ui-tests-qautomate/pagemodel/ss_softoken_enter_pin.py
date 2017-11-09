# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_softoken_enter_pin(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160330125409
    # Pagemodel url: https://test-rh1.i.palveluvayla.com:4000/keys
    # Pagemodel area: (271, 1, 1640, 302)
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
    PLEASE_ENTER_SOFTTOKEN_PIN = (By.CSS_SELECTOR, u'p>a') # x: 883 y: 10 width: 154 height: 17, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://test-rh1.i.palveluvayla.com:4000/keys
    ID_HEADING = (By.ID, u'heading') # x: 290 y: 51 width: 184 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    KEYS_FILTER_TEXT = (By.CSS_SELECTOR, u'#keys_filter>label>input') # x: 346 y: 113 width: 179 height: 33, tag: input, type: text, name: None, form_id: , checkbox: , table_id: , href:
    CERTIFICATE = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 291 y: 152 width: 613 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: keys, href:
    MEMBER = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[2]') # x: 904 y: 152 width: 613 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: keys, href:
    OCSP_RESPONSE = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[3]') # x: 1517 y: 152 width: 88 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: keys, href:
    EXPIRES = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[4]') # x: 1605 y: 152 width: 94 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: keys, href:
    STATUS = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[5]') # x: 1699 y: 152 width: 106 height: 54, tag: th, type: , name: None, form_id: , checkbox: , table_id: keys, href:
    TOKEN_NAME_SOFT_0 = (By.CSS_SELECTOR, u'.token-name') # x: 296 y: 212 width: 1278 height: 19, tag: div, type: , name: None, form_id: , checkbox: , table_id: keys, href:
    ACTIVATE_TOKEN_ENTER_PIN = (By.CSS_SELECTOR, u'.activate_token') # x: 1798 y: 212 width: 96 height: 46, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: keys, href:
    ID_DETAILS = (By.ID, u'details') # x: 290 y: 275 width: 78 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_GENERATE_KEY = (By.ID, u'generate_key') # x: 372 y: 275 width: 125 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_GENERATE_CSR = (By.ID, u'generate_csr') # x: 501 y: 275 width: 254 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_DISABLE = (By.ID, u'disable') # x: 759 y: 275 width: 81 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_REGISTER = (By.ID, u'register') # x: 843 y: 275 width: 89 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_DELETE = (By.ID, u'delete') # x: 936 y: 275 width: 74 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_IMPORT_CERT = (By.ID, u'import_cert') # x: 1732 y: 275 width: 168 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:

    def click_button_activate_token_enter_pin(self):
        """
        Click button to activate token pin
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ACTIVATE_TOKEN_ENTER_PIN*
        """
        # AutoGen method
        self.click_element(self.ACTIVATE_TOKEN_ENTER_PIN)

    def wait_until_softoken_pin_query_is_not_visible(self):
        """
        Wait until softoken pin query is visible
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_not_visible`, *self.PLEASE_ENTER_SOFTTOKEN_PIN*
        """
        self.wait_until_element_is_not_visible(self.PLEASE_ENTER_SOFTTOKEN_PIN)
