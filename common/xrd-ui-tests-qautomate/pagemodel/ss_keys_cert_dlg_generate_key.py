# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_keys_cert_dlg_generate_key(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160928083145
    # Pagemodel url: https://xroad-lxd-ss1.lxd:4000keys
    # Pagemodel area: (682, 400, 557, 170)
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
    MENUBAR_CLOSE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[2]') # x: 1184 y: 404 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 3, href:
    ID_LABEL = (By.ID, u'label') # x: 755 y: 475 width: 462 height: 33, tag: input, type: text, name: label, form_id: , checkbox: , table_id: 3, href:
    BUTTON_CANCEL = (By.XPATH, u'//div[7]/div[3]/div[1]/button[2]') # x: 1098 y: 525 width: 77 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: 3, href:
    BUTTON_OK = (By.XPATH, u'//div[7]/div[3]/div[1]/button[1]') # x: 1185 y: 525 width: 45 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: 3, href:

    def generate_key_label(self, text='ta_generated_key_sign'):
        """
        Input text to cert field and click button to confirm dialog

        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_LABEL*, *text*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
        """
        self.input_text(self.ID_LABEL, text)
        self.click_element(self.BUTTON_OK)
