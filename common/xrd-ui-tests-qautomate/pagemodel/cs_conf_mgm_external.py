# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_conf_mgm_external(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160804132215
    # Pagemodel url: https://test-cs2.i.palveluvayla.com:4000/configuration_management
    # Pagemodel area: (272, 38, 1640, 826)
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
    ID_HEADING = (By.ID, u'heading') # x: 290 y: 51 width: 249 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    INTERNAL_CONFIGURATION = (By.ID, u'ui-id-3') # x: 856 y: 108 width: 171 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/configuration_management#source_tab
    EXTERNAL_CONFIGURATION = (By.ID, u'ui-id-4') # x: 1028 y: 108 width: 173 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/configuration_management#source_tab
    TRUSTED_ANCHORS = (By.ID, u'ui-id-5') # x: 1202 y: 108 width: 132 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/configuration_management#trusted_anchors_tab
    ANCHOR = (By.XPATH, u'//div[1]/div[1]/div[1]/span[1]') # x: 300 y: 163 width: 65 height: 26, tag: span, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href: None
    ID_GENERATE_SOURCE_ANCHOR = (By.ID, u'generate_source_anchor') # x: 1665 y: 163 width: 96 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_DOWNLOAD_SOURCE_ANCHOR = (By.ID, u'download_source_anchor') # x: 1771 y: 163 width: 109 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    HASH_SHA_224 = (By.XPATH, u'//div[1]/p[1]/label[1]') # x: 300 y: 206 width: 109 height: 21, tag: label, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href:
    BOX_ANCHOR_HASH_FILE_NOT_FOUND = (By.CSS_SELECTOR, u'div.box>p>.anchor-hash') # x: 413 y: 206 width: 145 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    GENERATED_0 = (By.XPATH, u'//div[1]/p[2]/label[1]') # x: 300 y: 237 width: 76 height: 21, tag: label, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href:
    BOX_ANCHOR_GENERATED_AT_FILE_NOT_FOUND = (By.CSS_SELECTOR, u'div.box>p>.anchor-generated_at') # x: 380 y: 237 width: 145 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    DOWNLOAD_URL = (By.XPATH, u'//div[2]/div[1]/span[1]') # x: 300 y: 308 width: 131 height: 26, tag: span, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href: None
    ID_CONF_URL = (By.ID, u'conf_url') # x: 300 y: 344 width: 326 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    SIGNING_KEYS = (By.XPATH, u'//div[3]/div[1]/span[1]') # x: 300 y: 415 width: 111 height: 26, tag: span, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href: None
    ID_GENERATE_SIGNING_KEY = (By.ID, u'generate_signing_key') # x: 1614 y: 415 width: 86 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_ACTIVATE_SIGNING_KEY = (By.ID, u'activate_signing_key') # x: 1709 y: 415 width: 87 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_DELETE_SIGNING_KEY = (By.ID, u'delete_signing_key') # x: 1806 y: 415 width: 74 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    DEVICE_ID_KEY = (By.XPATH, u'//div[3]/div[2]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 301 y: 459 width: 1306 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href:
    GENERATED = (By.XPATH, u'//div[3]/div[2]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[2]') # x: 1607 y: 459 width: 166 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href:
    UNKNOWN = (By.XPATH, u'//div[3]/div[2]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[3]') # x: 1773 y: 459 width: 106 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href:
    CONFIGURATION_PARTS = (By.XPATH, u'//div[1]/div[4]/div[1]/span[1]') # x: 300 y: 579 width: 176 height: 26, tag: span, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href: None
    ID_DOWNLOAD_CONF_PART = (By.ID, u'download_conf_part') # x: 1771 y: 579 width: 109 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    FILE = (By.XPATH, u'//div[4]/div[2]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 301 y: 623 width: 526 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href:
    CONTENT_IDENTIFIER = (By.XPATH, u'//div[4]/div[2]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[2]') # x: 827 y: 623 width: 526 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href:
    UPDATED = (By.XPATH, u'//div[4]/div[2]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[3]') # x: 1353 y: 623 width: 526 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: conf_parts, href:

    def click_button_id_generate_signing_key(self):
        """
        Click button to generate signing key
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_GENERATE_SIGNING_KEY*
        """
        # AutoGen method
        self.click_element(self.ID_GENERATE_SIGNING_KEY)

