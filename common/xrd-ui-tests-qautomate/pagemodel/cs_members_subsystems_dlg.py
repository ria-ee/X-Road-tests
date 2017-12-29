# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from variables import errors
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_members_subsystems_dlg(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20161010130954
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/
    # Pagemodel area: (460, 233, 1000, 507)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[21]/div[1]/div[1]/button[1]') # x: 1358 y: 236 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: DataTables_Table_2, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[@data-name=\'member_edit_dialog\']//div[@class=\'ui-dialog-buttonset\']/button[@data-name=\'close\']') # x: 1409 y: 236 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: DataTables_Table_2, href:
    BUTTON_DELETE_SUBSYSTEM = (By.CSS_SELECTOR, u'div.ui-dialog-titlebar.ui-widget-header.ui-corner-all.ui-helper-clearfix.ui-draggable-handle>div.ui-tabs-panel-actions>#delete_subsystem') # x: 1213 y: 244 width: 74 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    BUTTON_ADD = (By.CSS_SELECTOR, u'div.ui-dialog-titlebar.ui-widget-header.ui-corner-all.ui-helper-clearfix.ui-draggable-handle>div.ui-tabs-panel-actions>#add_subsystem') # x: 1290 y: 244 width: 53 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    TITLE = (By.ID, u'ui-id-26') # x: 470 y: 250 width: 113 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    MEMBER_DETAILS = (By.ID, u'ui-id-27') # x: 536 y: 302 width: 129 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    OWNED_SERVERS = (By.ID, u'ui-id-28') # x: 666 y: 302 width: 124 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    GLOBAL_GROUP_MEMBERSHIP = (By.ID, u'ui-id-29') # x: 791 y: 302 width: 202 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    SUBSYSTEMS = (By.ID, u'ui-id-30') # x: 994 y: 302 width: 101 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    MANAGEMENT_REQUESTS = (By.ID, u'ui-id-32') # x: 1207 y: 302 width: 177 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    BUTTON_CLOSE = (By.XPATH, u'//div[21]/div[3]/div[1]/button[1]') # x: 1388 y: 694 width: 67 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: DataTables_Table_2, href:



    def click_button_submit(self):
        """
        Click button to submit dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.MENUBAR_CLOSE*
        """
        # AutoGen method
        self.click_element(self.MENUBAR_CLOSE)

    def click_button_add(self):
        """
        Click button to add

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_ADD*
        """
        # AutoGen method
        self.click_element(self.BUTTON_ADD)

    def click_element_in_subsystems_table(self, text=u'MANAGEMENT'):
        """
        Click subsystem from subsystems table with text

        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *element*
        """
        self.wait_until_jquery_ajax_loaded()
        # Element search
        locator = (By.ID, u'DataTables_Table_2')
        value = text
        row = u'TBODY/TR'
        cell = u'TD'
        self.wait_until_jquery_ajax_loaded()
        element_info = self.get_table_column_and_row_by_text(locator, value, row, cell)

        # Searched element info
        row_number = element_info[2]
        column_number = element_info[3]
        row_element = element_info[0]
        element = element_info[1]

        self.click_element(element)

        return element

    def check_subsystem_is_red(self, text=u'MANAGEMENT'):
        """
        Click and verify subsystem is red in subsystems dialog

        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.fail`, *errors.subsystem_not_red*
        """
        element = self.click_element_in_subsystems_table(text)
        if element.value_of_css_property("color") != "rgb(255, 0, 0)":
            self.fail(errors.subsystem_not_red)

    def sub_delete_is_enabled(self):
        """
        Verify subsystem delete button is enabled

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.fail`, *errors.subsystem_deletion_disabled*
        """
        if not self.is_enabled(self.BUTTON_DELETE_SUBSYSTEM):
            self.fail(errors.subsystem_deletion_disabled)
