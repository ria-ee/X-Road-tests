# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from variables import errors
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_backup_restore(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160330092952
    # Pagemodel url: https://test-cs.i.palveluvayla.com:4000/backup
    # Pagemodel area: (270, 0, 1647, 775)
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
    ID_BACKUP = (By.ID, u'backup') # x: 1346 y: 8 width: 207 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_BACKUP_UPLOAD = (By.ID, u'backup_upload') # x: 1560 y: 8 width: 175 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_HEADING = (By.ID, u'heading') # x: 290 y: 14 width: 178 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    BACKUP_ACTIONS = (By.CSS_SELECTOR, u'.backup_actions') # x: 290 y: 70 width: 1610 height: 0, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href:
    BACKUP_FILES_FILTER_TEXT = (By.CSS_SELECTOR, u'#backup_files_filter>label>input') # x: 346 y: 76 width: 179 height: 33, tag: input, type: text, name: None, form_id: , checkbox: , table_id: , href:

    # Dynamic objects:
    NEWEST_RESTORE = (By.XPATH, u'//td[2]/button[2]') # x: 1730 y: 190 width: 86 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href: # Dynamic object
    NEWEST_DELETE = (By.XPATH, u'//td[2]/button[1]') # x: 1821 y: 190 width: 73 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href: # Dynamic object
    BACKUP_FILES = (By.ID, u'backup_files') # x: 291 y: 114 width: 1608 height: 43, tag: table, type: , name: None, form_id: , checkbox: , table_id: , href:
    NEWEST_BACKUP_NAME = (By.XPATH, u'//div[2]/table[1]/tbody[1]/tr[1]/td[1]') # x: 291 y: 114 width: 804 height: 43, tag: td, type: , name: None, form_id: , checkbox: , table_id: , href:
    NEWEST_DOWNLOAD = (By.XPATH, u'//td[2]/button[3]') # x: 1821 y: 119 width: 73 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:

    def click_button_id_backup(self):
        """
        Click button to generate backup

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_BACKUP*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # AutoGen method
        self.click_element(self.ID_BACKUP)
        self.wait_until_jquery_ajax_loaded()
        TESTDATA[u'paths'][u'backup_file'] = self.get_text(self.NEWEST_BACKUP_NAME)

    def click_element_newest_restore(self):
        """
        Click restore button on backups tables first row

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.NEWEST_RESTORE*
        """
        self.click_element(self.NEWEST_RESTORE)

    def click_element_newest_delete(self):
        """
        Click delete button on backups tables first row

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.NEWEST_DELETE*
        """
        self.click_element(self.NEWEST_DELETE)

    def verify_contains_all_user_actions(self, parameters=None):
        """
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_should_be_present`, *self.ID_BACKUP*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_should_be_present`, *self.ID_BACKUP_UPLOAD*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.fail`, *errors.backup_name_is_empty*
            * **Step 4:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_should_be_present`, *self.NEWEST_RESTORE*
            * **Step 5:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_should_be_present`, *self.NEWEST_DELETE*
            * **Step 6:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_should_be_present`, *self.NEWEST_DOWNLOAD*
        """
        self.element_should_be_present(self.ID_BACKUP)
        self.element_should_be_present(self.ID_BACKUP_UPLOAD)
        backup_file = self.get_text(self.NEWEST_BACKUP_NAME)
        if not backup_file:
            self.fail(errors.backup_name_is_empty)
        self.element_should_be_present(self.NEWEST_RESTORE)
        self.element_should_be_present(self.NEWEST_DELETE)
        self.element_should_be_present(self.NEWEST_DOWNLOAD)

    def click_element_newest_download(self, parameters=None):
        """
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.NEWEST_DOWNLOAD*
        """
        self.click_element(self.NEWEST_DOWNLOAD)

    def click_element_upload_backup_file(self, parameters=None):
        """
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_BACKUP_UPLOAD*
        """
        self.click_element(self.ID_BACKUP_UPLOAD)
