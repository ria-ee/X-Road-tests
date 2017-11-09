# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = self.get_current_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_backup_restore(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20170309213708
    # Pagemodel url: https://xroad-lxd-ss2.lxd:4000/backup
    # Pagemodel area: (272, 54, 1632, 865)
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
    ID_BACKUP = (By.ID, u'backup') # x: 1334 y: 62 width: 215 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_BACKUP_UPLOAD = (By.ID, u'backup_upload') # x: 1556 y: 62 width: 180 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_HEADING = (By.ID, u'heading') # x: 290 y: 68 width: 181 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    BACKUP_ACTIONS = (By.CSS_SELECTOR, u'.backup_actions') # x: 290 y: 124 width: 1610 height: 0, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href:
    BACKUP_FILES_FILTER_TEXT = (By.CSS_SELECTOR, u'#backup_files_filter>label>input') # x: 346 y: 130 width: 203 height: 32, tag: input, type: text, name: None, form_id: , checkbox: , table_id: , href:
    DATA_TABLES_EMPTY_NO_MATCHING_RECORDS = (By.CSS_SELECTOR, u'.dataTables_empty') # x: 291 y: 168 width: 1608 height: 30, tag: td, type: , name: None, form_id: , checkbox: , table_id: backup_files, href:
    # Dynamic objects:
    FIRST_ROW_DELETE = (By.XPATH, u'//td[2]/button[1]') # x: 1821 y: 156 width: 73 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    FIRST_ROW_RESTORE = (By.XPATH, u'//td[2]/button[2]') # x: 1730 y: 156 width: 86 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:

    def click_button_id_backup(self, parameters=None):
        """
        Click button to generate backup

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_BACKUP*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # AutoGen method
        self.click_element(self.ID_BACKUP)
        self.wait_until_jquery_ajax_loaded()

    def click_element_first_row_restore(self):
        """
        Click restore button on first row in backups table

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.FIRST_ROW_RESTORE*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        self.click_element(self.FIRST_ROW_RESTORE)
        self.wait_until_jquery_ajax_loaded()

    def click_element_first_row_delete(self):
        """
        Click delete button on first row in backups table

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.FIRST_ROW_DELETE*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        self.click_element(self.FIRST_ROW_DELETE)
        self.wait_until_jquery_ajax_loaded()
