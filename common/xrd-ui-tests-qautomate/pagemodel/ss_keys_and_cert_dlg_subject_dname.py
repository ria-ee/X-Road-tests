# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_keys_and_cert_dlg_subject_dname(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160928092046
    # Pagemodel url: https://fdev-ss1.i.palveluvayla.com:4000/keys
    # Pagemodel area: (680, 330, 560, 307)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[8]/div[1]/div[1]/button[1]') # x: 1133 y: 336 width: 51 height: 49, tag: button, type: submit, name: None, form_id: keys, checkbox: , table_id: 4, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[8]/div[1]/div[1]/button[2]') # x: 1184 y: 336 width: 51 height: 49, tag: button, type: submit, name: None, form_id: keys, checkbox: , table_id: 4, href:
    NAME_C_UI_STATE_DISABLED_FI_TEXT = (By.CSS_SELECTOR, u'input[name="C"].ui-state-disabled') # x: 877 y: 410 width: 340 height: 33, tag: input, type: text, name: C, form_id: keys, checkbox: , table_id: 4, href:
    NAME_O_GOFORE_TEXT = (By.CSS_SELECTOR, u'input[name="O"]') # x: 877 y: 453 width: 340 height: 33, tag: input, type: text, name: O, form_id: keys, checkbox: , table_id: 4, href:
    NAME_SERIAL_NUMBER_UI_STATE_DISABLED_FI_COM_TEXT = (By.CSS_SELECTOR, u'input[name="serialNumber"].ui-state-disabled') # x: 877 y: 496 width: 340 height: 33, tag: input, type: text, name: serialNumber, form_id: keys, checkbox: , table_id: 4, href:
    NAME_CN_1234_TEXT = (By.CSS_SELECTOR, u'input[name="CN"]') # x: 877 y: 539 width: 340 height: 33, tag: input, type: text, name: CN, form_id: keys, checkbox: , table_id: 4, href:
    BUTTON_CANCEL = (By.XPATH, u'//div[9]/div[3]/div[1]/button[2]') # x: 1098 y: 590 width: 77 height: 37, tag: button, type: button, name: None, form_id: keys, checkbox: , table_id: 4, href:
    BUTTON_OK = (By.XPATH, u'//div[9]/div[3]/div[1]/button[1]') # x: 1185 y: 590 width: 45 height: 37, tag: button, type: button, name: None, form_id: keys, checkbox: , table_id: 4, href:

    def fill_input_values_keys_dname_sign(self, parameters=None):
        """
        Input random text to dna name field

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.NAME_O_GOFORE_TEXT*, *parameters['member_name'] + rword*
        """
        import random, string
        rword = ''.join(random.choice(string.lowercase) for i in range(4))
        self.input_text(self.NAME_O_GOFORE_TEXT, parameters['member_name'] + rword)

    def submit_keys_dname(self):
        """
        Click button to submit dnaname
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # AutoGen method submit form: keys
        self.click_element(self.BUTTON_OK)
        self.wait_until_jquery_ajax_loaded()

    def fill_input_values_keys_dname_auth(self, parameters=None):
        """
        Input random text to dna name field
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.NAME_O_GOFORE_TEXT*, *parameters['member_name'] + rword*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.NAME_CN_1234_TEXT*, *parameters['server_address']*
        """
        # AutoGen methods form: keys
        import random, string
        rword = ''.join(random.choice(string.lowercase) for i in range(4))
        self.input_text(self.NAME_O_GOFORE_TEXT, parameters['member_name'] + rword)
        self.input_text(self.NAME_CN_1234_TEXT, parameters['server_address'])
