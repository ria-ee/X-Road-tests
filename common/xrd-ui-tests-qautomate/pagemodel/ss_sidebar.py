# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_sidebar(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160928101910
    # Pagemodel url: https://xroad-lxd-ss1.lxd:4000/clients
    # Pagemodel area: (1, 0, 273, 526)
    # Pagemodel screen resolution: (1920, 1080)
    # Use project settings: True
    # Used filters: id, css_selector, class_name, link_text, xpath
    # Xpath type: xpath-position
    # Depth of css path: 3
    # Minimize css selector: True
    # Create automated methods: True
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
    XROAD_ID_FI_UI = (By.CSS_SELECTOR, u'h1>.xroad-id') # x: 20 y: 7 width: 42 height: 23, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    SERVER_INFO_SECURITY = (By.CSS_SELECTOR, u'#server-info>h2') # x: 0 y: 28 width: 270 height: 13, tag: h2, type: , name: None, form_id: , checkbox: , table_id: , href:
    DATA_NAME_CLIENTS_SECURITY_SERVER = (By.CSS_SELECTOR, u'a[data-name="clients"]') # x: 20 y: 99 width: 138 height: 18, tag: a, type: , name: clients, form_id: , checkbox: , table_id: , href: None
    DATA_NAME_SYSPARAMS_SYSTEM_PARAMETERS = (By.CSS_SELECTOR, u'a[data-name="sysparams"]') # x: 20 y: 127 width: 120 height: 18, tag: a, type: , name: sysparams, form_id: , checkbox: , table_id: , href: None
    DATA_NAME_KEYS_AND_CERTIFICATES = (By.CSS_SELECTOR, u'a[data-name="keys"]') # x: 20 y: 230 width: 129 height: 18, tag: a, type: , name: keys, form_id: , checkbox: , table_id: , href: None
    DATA_NAME_BACKUP_BACK_UP_AND_RESTORE = (By.CSS_SELECTOR, u'a[data-name="backup"]') # x: 20 y: 258 width: 129 height: 18, tag: a, type: , name: backup, form_id: , checkbox: , table_id: , href: None
    DATA_NAME_DIAGNOSTICS = (By.CSS_SELECTOR, u'a[data-name="diagnostics"]') # x: 20 y: 286 width: 71 height: 18, tag: a, type: , name: diagnostics, form_id: , checkbox: , table_id: , href: None
    DATA_NAME_ABOUT_VERSION = (By.CSS_SELECTOR, u'a[data-name="about"]') # x: 20 y: 388 width: 47 height: 18, tag: a, type: , name: about, form_id: , checkbox: , table_id: , href: None

    def verify_sidebar_title(self):
        """
        Verify sidebar title is visible on the page
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.SERVER_INFO_SECURITY*
        """
        self.wait_until_element_is_visible(self.SERVER_INFO_SECURITY)

    def click_keys_and_certificates(self):
        """
        Click sidebar link to open keys and certificates view

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DATA_NAME_KEYS_AND_CERTIFICATES*
        """
        self.click_element(self.DATA_NAME_KEYS_AND_CERTIFICATES)

    def click_element_data_name_sysparams_system_parameters(self):
        """
        Click sidebar link to open system parameters view

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DATA_NAME_SYSPARAMS_SYSTEM_PARAMETERS*
        """
        self.click_element(self.DATA_NAME_SYSPARAMS_SYSTEM_PARAMETERS)

    def click_element_security_server_clients(self):
        """
        Click sidebar link to open server clients view
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DATA_NAME_CLIENTS_SECURITY_SERVER*
        """
        self.click_element(self.DATA_NAME_CLIENTS_SECURITY_SERVER)

    def click_element_backup_and_restore(self):
        """
        Click sidebar link to open backups view

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DATA_NAME_BACKUP_BACK_UP_AND_RESTORE*
        """
        self.click_element(self.DATA_NAME_BACKUP_BACK_UP_AND_RESTORE)

    def click_element_diagnostics(self):
        """
        Click sidebar link to open diagnostics view
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DATA_NAME_DIAGNOSTICS*
        """
        self.click_element(self.DATA_NAME_DIAGNOSTICS)

    def click_element_version(self):
        """
        Click sidebar link to open version view
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DATA_NAME_ABOUT_VERSION*
        """
        self.click_element(self.DATA_NAME_ABOUT_VERSION)
