# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_member_details_owned_servers(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160426092749
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/
    # Pagemodel area: (460, 233, 1002, 506)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[21]/div[1]/div[1]/button[1]') # x: 1358 y: 235 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: DataTables_Table_5, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[21]/div[1]/div[1]/button[2]') # x: 1409 y: 235 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: DataTables_Table_5, href:
    BUTTON_ADD = (By.CSS_SELECTOR, u'div.ui-dialog-titlebar.ui-widget-header.ui-corner-all.ui-helper-clearfix.ui-draggable-handle>div.ui-tabs-panel-actions>#add_owned_server') # x: 1290 y: 243 width: 53 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    TITLE = (By.ID, u'ui-id-35') # x: 470 y: 249 width: 113 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    MEMBER_DETAILS = (By.ID, u'ui-id-36') # x: 536 y: 301 width: 129 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    OWNED_SERVERS = (By.ID, u'ui-id-37') # x: 666 y: 301 width: 124 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    GLOBAL_GROUP_MEMBERSHIP = (By.ID, u'ui-id-38') # x: 791 y: 301 width: 202 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    SUBSYSTEMS = (By.ID, u'ui-id-39') # x: 994 y: 301 width: 101 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    USED_SERVERS = (By.ID, u'ui-id-40') # x: 1096 y: 301 width: 110 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    MANAGEMENT_REQUESTS = (By.ID, u'ui-id-41') # x: 1207 y: 301 width: 177 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    SERVER = (By.XPATH, u'//div[2]/div[1]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 476 y: 347 width: 969 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: DataTables_Table_5, href:
    BUTTON_CLOSE = (By.XPATH, u'//div[21]/div[3]/div[1]/button[1]') # x: 1388 y: 693 width: 67 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: DataTables_Table_5, href:

    # Dynamic objects:

    def click_button_ui_titlebar_widget_corner_all_helper_clearfix_draggable_handle_tabs(self):
        """
        Click button to add owned server
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_ADD*
        """
        # AutoGen method
        self.click_element(self.BUTTON_ADD)

    def click_element_owned_server(self, parameters=None):
        """
        Click owned server link with parameters u'security_server_code'
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *(By.LINK_TEXT*, *parameters[u'security_server_code']*
        """
        self.click_element((By.LINK_TEXT, parameters[u'security_server_code']))
