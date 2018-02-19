# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = self.get_current_driver() e.g driver.current_url
from webframework import TESTDATA
from variables import strings
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_system_settings_change_cs_address_dlg(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20170522033143
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/system_settings
    # Pagemodel area: (713, 418, 501, 155)
    # Pagemodel screen resolution: (3840, 1080)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[1]') # x: 1108 y: 417 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: member_classes, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[2]') # x: 1159 y: 417 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: member_classes, href:
    TITLE = (By.ID, u'ui-id-3') # x: 720 y: 431 width: 165 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    ID_CENTRAL_SERVER_ADDRESS_NEW = (By.ID, u'central_server_address_new') # x: 725 y: 482 width: 473 height: 32, tag: input, type: text, name: central_server_address_new, form_id: , checkbox: , table_id: , href:
    # Dynamic objects:
    BUTTON_OK = (By.XPATH, u'(//button[@data-name=\'ok\' and @type=\'button\'])[3]') # x: 1161 y: 514 width: 44 height: 36, tag: button, type: button, name: ok, form_id: , checkbox: , table_id: , href:
    BUTTON_CANCEL = (By.XPATH, u'(//button[@data-name=\'cancel\' and @type=\'button\'])[3]') # x: 1076 y: 514 width: 75 height: 36, tag: button, type: button, name: cancel, form_id: , checkbox: , table_id: , href:

    def input_server_address(self, parameters=None):
        """
        Input text to server address field. Parameter used is 'server_address'
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_CENTRAL_SERVER_ADDRESS_NEW*, *parameters[u'server_address']*
        """
        server_address = parameters['server_address']
        if strings.server_environment_type() == strings.lxd_type_environment:
            server_address = server_address.replace("user@", "")
        self.input_text(self.ID_CENTRAL_SERVER_ADDRESS_NEW, server_address)

    def click_confim(self):
        """
        Click button to confirm the dialog
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
        """
        self.click_element(self.BUTTON_OK)

    def click_cancel(self):
        """
        Click button to cancel the dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_CANCEL*
        """
        self.click_element(self.BUTTON_CANCEL)
