# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from variables import strings
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_keys_and_cert_dlg_registration_req(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160930142412
    # Pagemodel url: https://xroad-lxd-ss1.lxd:4000/keys
    # Pagemodel area: (710, 387, 504, 201)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[13]/div[1]/div[1]/button[1]') # x: 1108 y: 386 width: 51 height: 49, tag: button, type: submit, name: None, form_id: keys, checkbox: , table_id: 3, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[13]/div[1]/div[1]/button[2]') # x: 1159 y: 386 width: 51 height: 49, tag: button, type: submit, name: None, form_id: keys, checkbox: , table_id: 3, href:
    TITLE = (By.ID, u'ui-id-9') # x: 720 y: 400 width: 144 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    ID_ADDRESS = (By.ID, u'address') # x: 1014 y: 456 width: 178 height: 33, tag: input, type: text, name: address, form_id: keys, checkbox: , table_id: 3, href:
    BUTTON_CANCEL = (By.XPATH, u'//div[13]/div[3]/div[1]/button[2]') # x: 1073 y: 544 width: 77 height: 37, tag: button, type: button, name: None, form_id: keys, checkbox: , table_id: 3, href:
    BUTTON_OK = (By.XPATH, u'//div[13]/div[3]/div[1]/button[1]') # x: 1160 y: 544 width: 45 height: 37, tag: button, type: button, name: None, form_id: keys, checkbox: , table_id: 3, href:

    def input_text_to_server_address(self, parameters=None):
        """
        Input text to server address field
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_ADDRESS*, *parameters['server_address']*
        """
        # AutoGen methods form: keys
        server_address = parameters['server_address']
        if strings.server_environment_type() == strings.lxd_type_environment:
            server_address = server_address.replace("user@", "")
        self.input_text(self.ID_ADDRESS, server_address)

    def submit_register_request(self):
        """
        Click button to confirm request
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # AutoGen method submit form: keys
        self.click_element(self.BUTTON_OK)
        self.wait_until_jquery_ajax_loaded()
