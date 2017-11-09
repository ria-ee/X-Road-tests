# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_sec_servers_new_client_req(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20151215140552
    # Pagemodel url: https://dev-cs.palveluvayla.com:4000/securityservers
    # Pagemodel area: (680, 186, 561, 598)
    # Pagemodel screen resolution: (1920, 1080)
    # Use project settings: True
    # Used filters: id, css_selector, class_name, link_text, xpath
    # Depth of css path: 8
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
    # Links found: 2
    # Page model constants:
    ID_SECURITYSERVERS = (By.ID, u'securityservers') # x: 291 y: 153 width: 1608 height: 383
    UI_ACTION_MAXIMIZE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-maximize') # x: 1138 y: 187 width: 51 height: 49
    UI_ACTION_CLOSE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-close') # x: 1189 y: 187 width: 51 height: 49
    TITLE = (By.ID, u'ui-id-11') # x: 690 y: 201 width: 227 height: 21
    SECURITYSERVER_CLIENT_REGISTER_BODY_CONTAINER_INFORMATION = (By.CSS_SELECTOR, u'#securityserver_client_register_dialog>.dialog-body>section.container>h2>span') # x: 705 y: 259 width: 165 height: 22
    ID_SECURITYSERVER_CLIENT_CLIENT_SEARCH = (By.ID, u'securityserver_client_client_search') # x: 710 y: 293 width: 78 height: 33
    ID_SECURITYSERVER_CLIENT_REGISTER_NAME = (By.XPATH, u'id(\'securityserver_client_register_dialog\')/DIV[1]/SECTION[1]/TABLE[1]/TBODY[1]/TR[2]/TD[1]') # x: 705 y: 331 width: 130 height: 42
    ID_SECURITYSERVER_CLIENT_NAME = (By.ID, u'securityserver_client_name') # x: 840 y: 336 width: 373 height: 32
    ID_SECURITYSERVER_CLIENT_REGISTER_CLASS = (By.XPATH, u'id(\'securityserver_client_register_dialog\')/DIV[1]/SECTION[1]/TABLE[1]/TBODY[1]/TR[3]/TD[1]') # x: 705 y: 373 width: 130 height: 42
    ID_SECURITYSERVER_CLIENT_REGISTER = (By.XPATH, u'id(\'securityserver_client_register_dialog\')/DIV[1]/SECTION[1]/TABLE[1]/TBODY[1]/TR[4]/TD[1]') # x: 705 y: 415 width: 130 height: 42
    ID_SECURITYSERVER_CLIENT_CODE = (By.ID, u'securityserver_client_code') # x: 840 y: 420 width: 373 height: 32
    ID_SECURITYSERVER_CLIENT_REGISTER_SUBSYSTEM = (By.XPATH, u'id(\'securityserver_client_register_dialog\')/DIV[1]/SECTION[1]/TABLE[1]/TBODY[1]/TR[5]/TD[1]') # x: 705 y: 457 width: 130 height: 43
    ID_SECURITYSERVER_CLIENT_SUBSYSTEM_CODE = (By.ID, u'securityserver_client_subsystem_code') # x: 840 y: 462 width: 373 height: 33
    ID_SECURITYSERVER_CLIENT_REGISTER_OWNER_NAME = (By.XPATH, u'id(\'securityserver_client_register_dialog\')/DIV[1]/SECTION[2]/TABLE[1]/TBODY[1]/TR[1]/TD[1]') # x: 705 y: 546 width: 130 height: 43
    ID_SECURITYSERVER_CLIENT_OWNER_NAME = (By.ID, u'securityserver_client_owner_name') # x: 840 y: 551 width: 373 height: 33
    ID_SECURITYSERVER_CLIENT_REGISTER_OWNER_CLASS = (By.XPATH, u'id(\'securityserver_client_register_dialog\')/DIV[1]/SECTION[2]/TABLE[1]/TBODY[1]/TR[2]/TD[1]') # x: 705 y: 589 width: 130 height: 43
    ID_SECURITYSERVER_CLIENT_OWNER_CLASS = (By.ID, u'securityserver_client_owner_class') # x: 840 y: 594 width: 373 height: 33
    ID_SECURITYSERVER_CLIENT_REGISTER_OWNER = (By.XPATH, u'id(\'securityserver_client_register_dialog\')/DIV[1]/SECTION[2]/TABLE[1]/TBODY[1]/TR[3]/TD[1]') # x: 705 y: 632 width: 130 height: 43
    ID_SECURITYSERVER_CLIENT_OWNER_CODE = (By.ID, u'securityserver_client_owner_code') # x: 840 y: 637 width: 373 height: 33
    ID_SECURITYSERVER_CLIENT_REGISTER_SERVER = (By.XPATH, u'id(\'securityserver_client_register_dialog\')/DIV[1]/SECTION[2]/TABLE[1]/TBODY[1]/TR[4]/TD[1]') # x: 705 y: 675 width: 130 height: 43
    ID_SECURITYSERVER_CLIENT_SERVER_CODE = (By.ID, u'securityserver_client_server_code') # x: 840 y: 680 width: 373 height: 33
    BUTTON_CANCEL = (By.CSS_SELECTOR, u'button[data-name="cancel"]') # x: 1072 y: 741 width: 77 height: 37
    BUTTON_CONFIRM = (By.ID, u'securityserver_client_register_submit') # x: 1159 y: 741 width: 76 height: 37

    def click_new_client_search(self):
        """
        Click new cliants search
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_SECURITYSERVER_CLIENT_CLIENT_SEARCH*
        """
        self.click_element(self.ID_SECURITYSERVER_CLIENT_CLIENT_SEARCH)

    def insert_subsystem_code(self, parameters=None):
        """
        Input subsystem code to dialog. Parameter used is 'subsystem_code'
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_SECURITYSERVER_CLIENT_SUBSYSTEM_CODE*, *parameters[u'subsystem_code']*
        """
        self.input_text(self.ID_SECURITYSERVER_CLIENT_SUBSYSTEM_CODE, parameters[u'subsystem_code'])

    def click_submit_new_client_request(self):
        """
        Click button to submit dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_CONFIRM*
        """
        self.click_element(self.BUTTON_CONFIRM)