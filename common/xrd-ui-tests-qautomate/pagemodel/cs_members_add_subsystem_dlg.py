# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_members_add_subsystem_dlg(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20161010131303
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/
    # Pagemodel area: (710, 386, 502, 205)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[24]/div[1]/div[1]/button[1]') # x: 1108 y: 386 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: member_to_group_add_subsystem, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[24]/div[1]/div[1]/button[2]') # x: 1159 y: 386 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: member_to_group_add_subsystem, href:
    TITLE = (By.ID, u'ui-id-34') # x: 720 y: 400 width: 109 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    SUBSYSTEM = (By.XPATH, u'//div[2]/div[1]/form[1]/table[1]/tbody[1]/tr[1]/td[1]') # x: 725 y: 451 width: 186 height: 43, tag: td, type: , name: None, form_id: , checkbox: , table_id: member_to_group_add_subsystem, href:
    ID_SUBSYSTEM_ADD_CODE = (By.ID, u'subsystem_add_code') # x: 916 y: 456 width: 276 height: 33, tag: input, type: text, name: None, form_id: , checkbox: , table_id: member_to_group_add_subsystem, href:
    BUTTON_CANCEL = (By.XPATH, u'//div[24]/div[3]/div[1]/button[2]') # x: 1073 y: 544 width: 77 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: member_to_group_add_subsystem, href:
    BUTTON_OK = (By.ID, u'subsystem_add_submit') # x: 1160 y: 544 width: 45 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: , href:

    def input_text_to_id_subsystem_add_code(self, parameters=None):
        """
        Input text to subsystem code field. Using parameter 'subsystem_code'

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_SUBSYSTEM_ADD_CODE*, *parameters['subsystem_code']*
        """
        # AutoGen method
        self.input_text(self.ID_SUBSYSTEM_ADD_CODE, parameters['subsystem_code'])

    def click_button_id_subsystem_add_submit(self):
        """
        Click button to submit dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # AutoGen method
        self.click_element(self.BUTTON_OK)
        self.wait_until_jquery_ajax_loaded()