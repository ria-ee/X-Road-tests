# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_sec_servers_delete_clients(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20151215141120
    # Pagemodel url: https://dev-cs.palveluvayla.com:4000/securityservers
    # Pagemodel area: (730, 204, 461, 564)
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
    UI_ACTION_MAXIMIZE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-maximize') # x: 1088 y: 203 width: 51 height: 49
    UI_ACTION_CLOSE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-close') # x: 1139 y: 203 width: 51 height: 49
    TITLE = (By.ID, u'ui-id-17') # x: 740 y: 217 width: 166 height: 21
    SECURITYSERVER_CLIENT_REMOVE_BODY_CONTAINER_INFORMATION = (By.CSS_SELECTOR, u'#securityserver_client_remove_dialog>.dialog-body>section.container>legend') # x: 755 y: 278 width: 411 height: 30
    ID_SERVER_CLIENT_REMOVE_NAME = (By.ID, u'server_client_remove_name') # x: 1034 y: 313 width: 129 height: 33
    ID_SECURITYSERVER_CLIENT_REMOVE_CLASS = (By.XPATH, u'id(\'securityserver_client_remove_dialog\')/DIV[1]/SECTION[1]/TABLE[1]/TBODY[1]/TR[2]/TD[1]') # x: 755 y: 351 width: 274 height: 43
    ID_SERVER_CLIENT_REMOVE_CLASS = (By.ID, u'server_client_remove_class') # x: 1034 y: 356 width: 129 height: 33
    ID_SECURITYSERVER_CLIENT_REMOVE = (By.XPATH, u'id(\'securityserver_client_remove_dialog\')/DIV[1]/SECTION[1]/TABLE[1]/TBODY[1]/TR[3]/TD[1]') # x: 755 y: 394 width: 274 height: 43
    ID_SERVER_CLIENT_REMOVE_CODE = (By.ID, u'server_client_remove_code') # x: 1034 y: 399 width: 129 height: 33
    ID_SECURITYSERVER_CLIENT_REMOVE_SUBSYSTEM = (By.XPATH, u'id(\'securityserver_client_remove_dialog\')/DIV[1]/SECTION[1]/TABLE[1]/TBODY[1]/TR[4]/TD[1]') # x: 755 y: 437 width: 274 height: 43
    ID_SERVER_CLIENT_REMOVE_SUBSYSTEM_CODE = (By.ID, u'server_client_remove_subsystem_code') # x: 1034 y: 442 width: 129 height: 33
    ID_SECURITYSERVER_CLIENT_REMOVE_OWNER_NAME = (By.XPATH, u'id(\'securityserver_client_remove_dialog\')/DIV[1]/SECTION[2]/TABLE[1]/TBODY[1]/TR[1]/TD[1]') # x: 755 y: 530 width: 255 height: 43
    ID_SERVER_CLIENT_REMOVE_OWNER_NAME = (By.ID, u'server_client_remove_owner_name') # x: 1015 y: 535 width: 148 height: 33
    ID_SECURITYSERVER_CLIENT_REMOVE_OWNER_CLASS = (By.XPATH, u'id(\'securityserver_client_remove_dialog\')/DIV[1]/SECTION[2]/TABLE[1]/TBODY[1]/TR[2]/TD[1]') # x: 755 y: 573 width: 255 height: 43
    ID_SERVER_CLIENT_REMOVE_OWNER_CLASS = (By.ID, u'server_client_remove_owner_class') # x: 1015 y: 578 width: 148 height: 33
    ID_SECURITYSERVER_CLIENT_REMOVE_OWNER = (By.XPATH, u'id(\'securityserver_client_remove_dialog\')/DIV[1]/SECTION[2]/TABLE[1]/TBODY[1]/TR[3]/TD[1]') # x: 755 y: 616 width: 255 height: 43
    ID_SERVER_CLIENT_REMOVE_OWNER_CODE = (By.ID, u'server_client_remove_owner_code') # x: 1015 y: 621 width: 148 height: 33
    ID_SECURITYSERVER_CLIENT_REMOVE_SERVER = (By.XPATH, u'id(\'securityserver_client_remove_dialog\')/DIV[1]/SECTION[2]/TABLE[1]/TBODY[1]/TR[4]/TD[1]') # x: 755 y: 659 width: 255 height: 43
    ID_SERVER_CLIENT_REMOVE_SERVER_CODE = (By.ID, u'server_client_remove_server_code') # x: 1015 y: 664 width: 148 height: 33

    # Dynamic objects:
    BUTTON_SUBMIT = (By.XPATH, u'//div[18]/div[3]/div[1]/button[1]') # x: 1110 y: 717 width: 75 height: 36, tag: button, type: button, name: None, form_id: , checkbox: , table_id: , href: # Dynamic object

    def click_element_submit(self):
        """
        Click button to submit the dialog
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_SUBMIT*
        """
        self.click_element(self.BUTTON_SUBMIT)
