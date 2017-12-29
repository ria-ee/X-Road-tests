# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_members_details_dlg(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160330151543
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/
    # Pagemodel area: (460, 236, 1002, 501)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[21]/div[1]/div[1]/button[1]') # x: 1358 y: 235 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 3, href:
    DELETE = (By.XPATH, u'//div[21]/div[1]/div[2]/button[1]') # x: 1270 y: 243 width: 74 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 3, href:
    MEMBER_DETAILS = (By.ID, u'ui-id-27') # x: 536 y: 301 width: 129 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    OWNED_SERVERS = (By.ID, u'ui-id-28') # x: 666 y: 301 width: 124 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    GLOBAL_GROUP_MEMBERSHIP = (By.ID, u'ui-id-29') # x: 791 y: 301 width: 202 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    SUBSYSTEMS = (By.ID, u'ui-id-30') # x: 994 y: 301 width: 101 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    USED_SERVERS = (By.ID, u'ui-id-31') # x: 1096 y: 301 width: 110 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    MEMBER_NAME = (By.XPATH, u'//div[2]/div[1]/div[1]/div[1]/form[1]/table[1]/tbody[1]/tr[1]/td[1]') # x: 475 y: 346 width: 111 height: 43, tag: td, type: , name: None, form_id: , checkbox: , table_id: 3, href:
    TESTIFIRMA = (By.XPATH, u'//div[2]/div[1]/div[1]/div[1]/form[1]/table[1]/tbody[1]/tr[1]/td[2]/p[1]') # x: 591 y: 351 width: 788 height: 33, tag: p, type: , name: None, form_id: , checkbox: , table_id: 3, href:
    EDIT = (By.XPATH, u'//div[2]/div[1]/div[1]/div[1]/form[1]/table[1]/tbody[1]/tr[1]/td[3]/button[1]') # x: 1387 y: 351 width: 54 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 3, href:
    MEMBER_CLASS = (By.XPATH, u'//div[2]/div[1]/div[1]/div[1]/form[1]/table[1]/tbody[1]/tr[2]/td[1]') # x: 475 y: 389 width: 111 height: 43, tag: td, type: , name: None, form_id: , checkbox: , table_id: 3, href:
    GOV = (By.XPATH, u'//div[2]/div[1]/div[1]/div[1]/form[1]/table[1]/tbody[1]/tr[2]/td[2]/p[1]') # x: 591 y: 394 width: 788 height: 33, tag: p, type: , name: None, form_id: , checkbox: , table_id: 3, href:
    MEMBER = (By.XPATH, u'//div[2]/div[1]/div[1]/div[1]/form[1]/table[1]/tbody[1]/tr[3]/td[1]') # x: 475 y: 432 width: 111 height: 43, tag: td, type: , name: None, form_id: , checkbox: , table_id: 3, href:
    CONST_1234567_1 = (By.XPATH, u'//div[2]/div[1]/div[1]/div[1]/form[1]/table[1]/tbody[1]/tr[3]/td[2]/p[1]') # x: 591 y: 437 width: 788 height: 33, tag: p, type: , name: None, form_id: , checkbox: , table_id: 3, href:
    MESSAGE_FA_TIMES = (By.CSS_SELECTOR, u'.message>.fa-times') # x: 1430 y: 662 width: 20 height: 19, tag: i, type: , name: None, form_id: , checkbox: , table_id: , href:

    # Dynamic objects:
    MANAGEMENT_REQUESTS_TAB = (By.XPATH, u'(//*[contains(@href,\'#member_management_requests_tab\')])[2]') # x: 1210 y: 244 width: 177 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://xroad-lxd-cs.lxd:4000/#member_management_requests_tab
    CLASS_MESSAGE = (By.CLASS_NAME, u'message') # x: 460 y: 658 width: 1000 height: 30, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href: # Dynamic object
    BUTTON_CLOSE = (By.XPATH, u'(//div[@data-name="member_edit_dialog"]//button[@data-name="close"])[2]')  # x: 1390 y: 637 width: 65 height: 36 # Dynamic object

    def click_button_delete(self):
        """
        Click button to delete member
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DELETE*
        """
        # AutoGen method
        self.click_element(self.DELETE)

    def click_member_detail_tab(self):
        """
        Click tab to open member details in dialog
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.MEMBER_DETAILS*
        """
        self.click_element(self.MEMBER_DETAILS)

    def click_subsystems_tab(self):
        """
        Click tab to open subsystems view in dialog
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.SUBSYSTEMS*
        """
        self.click_element(self.SUBSYSTEMS)

    def click_button_close(self):
        """
        Click button to close the dialog
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_CLOSE*
        """
        # AutoGen method
        self.click_element(self.BUTTON_CLOSE)

    def click_element_owned_servers(self):
        """
        Click tab to open owned servers view in dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.OWNED_SERVERS*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        self.click_element(self.OWNED_SERVERS)
        self.wait_until_jquery_ajax_loaded()

    def wait_until_submitted_certificate(self):
        """
        Wait until certificate is submitted. Waiting for text u'Request of adding auth'
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_contains`, *self.CLASS_MESSAGE*, *u'Request of adding auth'*
        """
        self.wait_until_element_contains(self.CLASS_MESSAGE, u'Request of adding auth')

    def click_element_management_requests_tab(self):
        """
        Click tab to show management requests view in dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.MANAGEMENT_REQUESTS_TAB*
        """
        self.click_element(self.MANAGEMENT_REQUESTS_TAB)
