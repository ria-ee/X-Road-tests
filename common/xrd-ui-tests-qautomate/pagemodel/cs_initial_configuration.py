# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from variables import strings
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_initial_configuration(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160802084240
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/init
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
    CENTRAL_SERVER_IDENTIFICATION = (By.XPATH, u'//form[1]/h2[1]') # x: 610 y: 70 width: 700 height: 22, tag: h2, type: , name: None, form_id: init, checkbox: , table_id: 2, href:
    ID_INSTANCE_IDENTIFIER = (By.ID, u'instance_identifier') # x: 845 y: 97 width: 462 height: 33, tag: input, type: text, name: instance_identifier, form_id: init, checkbox: , table_id: 1, href:
    ID_CENTRAL_SERVER_ADDRESS = (By.ID, u'central_server_address') # x: 845 y: 140 width: 462 height: 33, tag: input, type: text, name: central_server_address, form_id: init, checkbox: , table_id: 1, href:
    SOFTWARE_TOKEN = (By.XPATH, u'//form[1]/h2[2]') # x: 610 y: 178 width: 700 height: 22, tag: h2, type: , name: None, form_id: init, checkbox: , table_id: 2, href:
    ID_PIN = (By.ID, u'pin') # x: 845 y: 205 width: 462 height: 33, tag: input, type: password, name: pin, form_id: init, checkbox: , table_id: 2, href:
    ID_PIN_REPEAT = (By.ID, u'pin_repeat') # x: 845 y: 248 width: 462 height: 33, tag: input, type: password, name: pin_repeat, form_id: init, checkbox: , table_id: 2, href:
    ID_SUBMIT = (By.ID, u'submit') # x: 1233 y: 296 width: 77 height: 33, tag: button, type: submit, name: None, form_id: init, checkbox: , table_id: , href:

    def fill_input_values_init(self, parameters=None):
        """
        Fill input values to initilization fields
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_INSTANCE_IDENTIFIER*, *parameters['instance_identifier']*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_CENTRAL_SERVER_ADDRESS*, *parameters['server_address']*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_PIN*, *parameters['pin']*
            * **Step 4:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_PIN_REPEAT*, *parameters['pin']*
        """
        # AutoGen methods form: init
        self.input_text(self.ID_INSTANCE_IDENTIFIER, parameters['instance_identifier'])
        server_address = parameters['server_address']
        if strings.server_environment_type() == strings.lxd_type_environment:
            server_address = server_address.replace("user@", "")
        self.input_text(self.ID_CENTRAL_SERVER_ADDRESS, server_address)
        self.input_text(self.ID_PIN, parameters['pin'])
        self.input_text(self.ID_PIN_REPEAT, parameters['pin'])

    def submit_init_noname1(self):
        """
        Submit the initilization values

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_SUBMIT*
        """
        # AutoGen method submit form: init
        self.click_element(self.ID_SUBMIT)