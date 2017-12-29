# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_initial_conf_server_details(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160330100340
    # Pagemodel url: https://xroad-lxd-ss1.lxd:4000:4000/init
    # Pagemodel area: Full screen
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
    ID_HEADING = (By.ID, u'heading') # x: 20 y: 14 width: 190 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    INIT_CONTAINER_IMPORT_CONFIGURATION_ANCHOR = (By.CSS_SELECTOR, u'#init-container>h2') # x: 610 y: 70 width: 700 height: 22, tag: h2, type: , name: None, form_id: , checkbox: , table_id: , href:
    CONFIGURATION_ANCHOR_TEST_INTERNAL_UTC_2016_03_01_12_14 = (By.XPATH, u'//section[1]/table[1]/tbody[1]/tr[1]/td[1]/input[1]') # x: 615 y: 97 width: 506 height: 33, tag: input, type: text, name: None, form_id: serverconf_form, checkbox: , table_id: 4, href:
    SECURITY_SERVER_OWNER = (By.XPATH, u'//form[1]/h2[1]') # x: 610 y: 135 width: 700 height: 22, tag: h2, type: , name: None, form_id: serverconf_form, checkbox: , table_id: 4, href:
    MEMBER_CLASS = (By.XPATH, u'//form[1]/table[1]/tbody[1]/tr[1]/td[1]') # x: 610 y: 157 width: 230 height: 45, tag: td, type: , name: None, form_id: serverconf_form, checkbox: , table_id: 4, href:
    ID_OWNER_CLASS = (By.ID, u'owner_class') # x: 845 y: 162 width: 461 height: 35, tag: select, type: , name: owner_class, form_id: serverconf_form, checkbox: , table_id: 2, href:
    MEMBER = (By.XPATH, u'//form[1]/table[1]/tbody[1]/tr[2]/td[1]') # x: 610 y: 202 width: 230 height: 43, tag: td, type: , name: None, form_id: serverconf_form, checkbox: , table_id: 4, href:
    ID_OWNER_CODE = (By.ID, u'owner_code') # x: 845 y: 207 width: 462 height: 33, tag: input, type: text, name: owner_code, form_id: serverconf_form, checkbox: , table_id: 2, href:
    MEMBER_NAME = (By.XPATH, u'//tr[3]/td[1]') # x: 610 y: 245 width: 230 height: 31, tag: td, type: , name: None, form_id: serverconf_form, checkbox: , table_id: 4, href:
    ID_OWNER_NAME = (By.ID, u'owner_name') # x: 840 y: 245 width: 470 height: 31, tag: td, type: , name: None, form_id: serverconf_form, checkbox: , table_id: 2, href:
    SECURITY_SERVER = (By.XPATH, u'//form[1]/h2[2]') # x: 610 y: 276 width: 700 height: 22, tag: h2, type: , name: None, form_id: serverconf_form, checkbox: , table_id: 4, href:
    SECURITY_SERVER_0 = (By.XPATH, u'//table[2]/tbody[1]/tr[1]/td[1]') # x: 610 y: 298 width: 230 height: 43, tag: td, type: , name: None, form_id: serverconf_form, checkbox: , table_id: 4, href:
    ID_SERVER_CODE = (By.ID, u'server_code') # x: 845 y: 303 width: 462 height: 33, tag: input, type: text, name: server_code, form_id: serverconf_form, checkbox: , table_id: 3, href:
    SOFTWARE_TOKEN = (By.XPATH, u'//form[1]/h2[3]') # x: 610 y: 341 width: 700 height: 22, tag: h2, type: , name: None, form_id: serverconf_form, checkbox: , table_id: 4, href:
    PIN = (By.XPATH, u'//table[3]/tbody[1]/tr[1]/td[1]') # x: 610 y: 363 width: 230 height: 43, tag: td, type: , name: None, form_id: serverconf_form, checkbox: , table_id: 4, href:
    ID_PIN = (By.ID, u'pin') # x: 845 y: 368 width: 462 height: 33, tag: input, type: password, name: pin, form_id: serverconf_form, checkbox: , table_id: 4, href:
    REPEAT_PIN = (By.XPATH, u'//table[3]/tbody[1]/tr[2]/td[1]') # x: 610 y: 406 width: 230 height: 43, tag: td, type: , name: None, form_id: serverconf_form, checkbox: , table_id: 4, href:
    ID_PIN_REPEAT = (By.ID, u'pin_repeat') # x: 845 y: 411 width: 462 height: 33, tag: input, type: password, name: pin_repeat, form_id: serverconf_form, checkbox: , table_id: 4, href:
    ID_SUBMIT_SERVERCONF = (By.ID, u'submit_serverconf') # x: 610 y: 459 width: 77 height: 33, tag: button, type: submit, name: None, form_id: serverconf_form, checkbox: , table_id: , href:

    def fill_input_values_serverconfform(self, parameters=None):
        """
        Fill input values server serverconfform

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_OWNER_CODE*, *parameters['member_code']*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_SERVER_CODE*, *parameters['security_server_code']*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.select_from_list_by_label`, *self.ID_OWNER_CLASS*, *parameters['member_class']*
        """
        # AutoGen methods form: serverconf_form
        sleep(2)
        self.input_text(self.ID_OWNER_CODE, parameters['member_code'])
        self.input_text(self.ID_SERVER_CODE, parameters['security_server_code'])
        self.select_from_list_by_label(self.ID_OWNER_CLASS, parameters['member_class'])

    def fill_input_values_pincode(self, parameters=None):
        """
        Fill pin code fields
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_PIN*, *parameters['pin']*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_PIN_REPEAT*, *parameters['pin']*
        """
        self.input_text(self.ID_PIN, parameters['pin'])
        self.input_text(self.ID_PIN_REPEAT, parameters['pin'])

    def submit_serverconfform_noname1(self):
        """
        Click button to confirm the dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_SUBMIT_SERVERCONF*
        """
        # AutoGen method submit form: serverconf_form
        self.click_element(self.ID_SUBMIT_SERVERCONF)

    def wait_until_element_is_visible_security_server_owner(self):
        """
        Wait until views is visible

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.SECURITY_SERVER_OWNER*
        """
        self.wait_until_element_is_visible(self.SECURITY_SERVER_OWNER)
