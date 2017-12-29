# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from variables import strings
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_keys_and_cert_generate_csr(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160928083427
    # Pagemodel url: https://xroad-lxd-ss1.lxd:4000/keys
    # Pagemodel area: (685, 333, 550, 303)
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
    BUTTON_MAXIMIZE = (By.XPATH, u'//div[8]/div[1]/div[1]/button[1]') # x: 1133 y: 336 width: 51 height: 49, tag: button, type: submit, name: None, form_id: keys, checkbox: , table_id: 3, href:
    TITLE = (By.ID, u'ui-id-4') # x: 695 y: 350 width: 259 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    ID_KEY_USAGE = (By.ID, u'key_usage') # x: 854 y: 406 width: 363 height: 35, tag: select, type: , name: None, form_id: keys, checkbox: , table_id: 3, href:
    ID_REGISTER = (By.ID, u'register') # x: 715 y: 448 width: 89 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    NAME_MEMBER_ID_FI_COM_1234 = (By.CSS_SELECTOR, u'select[name="member_id"]') # x: 854 y: 451 width: 363 height: 35, tag: select, type: , name: member_id, form_id: keys, checkbox: , table_id: 3, href:
    ID_APPROVED_CA = (By.ID, u'approved_ca') # x: 854 y: 496 width: 363 height: 35, tag: select, type: , name: None, form_id: keys, checkbox: , table_id: 3, href:
    ID_CSR_FORMAT = (By.ID, u'csr_format') # x: 854 y: 541 width: 363 height: 35, tag: select, type: , name: csr_format, form_id: keys, checkbox: , table_id: 3, href:
    BUTTON_CANCEL = (By.XPATH, u'//div[8]/div[3]/div[1]/button[2]') # x: 1098 y: 594 width: 77 height: 37, tag: button, type: button, name: None, form_id: keys, checkbox: , table_id: 3, href:
    BUTTON_OK = (By.ID, u'generate_csr_submit') # x: 1185 y: 594 width: 45 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: , href:

    def click_button_id_generate_csr_submit(self):
        """
        Click button to submit csr generation
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
        """
        # AutoGen method
        self.click_element(self.BUTTON_OK)

    def fill_input_values_keys_csr_sign(self, parameters=None):
        """
        Input text to keys csr signing

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.select_from_list_by_label`, *self.ID_KEY_USAGE*, *sign_key*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.select_from_list_by_label`, *self.NAME_MEMBER_ID_FI_COM_1234*, *member_id*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.select_from_list_by_label`, *self.ID_APPROVED_CA*, *approved_ca*
            * **Step 4:** :func:`~webframework.extension.util.common_utils.CommonUtils.select_from_list_by_label`, *self.ID_CSR_FORMAT*, *csr_format*
        """
        # AutoGen methods form: keys
        sign_key = strings.sign_key_usage
        csr_format = strings.server_environment_csr_format()
        approved_ca = strings.server_environment_approved_ca()
        member_id = strings.generate_member_id_short(parameters)

        self.select_from_list_by_label(self.ID_KEY_USAGE, sign_key)
        self.select_from_list_by_label(self.NAME_MEMBER_ID_FI_COM_1234, member_id)
        self.select_from_list_by_label(self.ID_APPROVED_CA, approved_ca)
        self.select_from_list_by_label(self.ID_CSR_FORMAT, csr_format)

    def fill_input_values_keys_csr_auth(self):
        """
        Input text to csr auth fields

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.select_from_list_by_label`, *self.ID_KEY_USAGE*, *auth_key*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.list_label_should_be`, *self.ID_KEY_USAGE*, *auth_key.upper(*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.select_from_list_by_label`, *self.ID_APPROVED_CA*, *approved_ca*
            * **Step 4:** :func:`~webframework.extension.util.common_utils.CommonUtils.select_from_list_by_label`, *self.ID_CSR_FORMAT*, *csr_format*
        """
        # AutoGen methods form: keys
        auth_key = strings.auth_key_usage
        csr_format = strings.server_environment_csr_format()
        approved_ca = strings.server_environment_approved_ca()

        self.select_from_list_by_label(self.ID_KEY_USAGE, auth_key)
        self.list_label_should_be(self.ID_KEY_USAGE, auth_key.upper())
        sleep(2)
        self.select_from_list_by_label(self.ID_APPROVED_CA, approved_ca)
        self.select_from_list_by_label(self.ID_CSR_FORMAT, csr_format)
