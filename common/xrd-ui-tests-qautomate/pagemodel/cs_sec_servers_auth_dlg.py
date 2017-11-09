# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_sec_servers_auth_dlg(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160301120420
    # Pagemodel url: https://dev-cs.palveluvayla.com:4000/securityservers
    # Pagemodel area: (713, 268, 501, 436)
    # Pagemodel screen resolution: (1920, 1080)
    # Use project settings: True
    # Used filters: id, css_selector, class_name, link_text, xpath
    # Xpath type: xpath-position
    # Create automated methods: True
    # Depth of css path: 4
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
    # Links found: 1
    # Page model constants:
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[9]/div[1]/div[1]/button[1]') # x: 1108 y: 267 width: 51 height: 49, tag: button, type: submit, name: None, form_id: server_auth_cert_upload, checkbox: , table_id: 6, href:
    TITLE = (By.ID, u'ui-id-9') # x: 720 y: 281 width: 213 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    SECURITY_SERVER = (By.XPATH, u'//div[9]/div[2]/div[1]/section[1]/legend[1]') # x: 735 y: 342 width: 451 height: 30, tag: legend, type: , name: None, form_id: server_auth_cert_upload, checkbox: , table_id: 6, href:
    ID_ADD_AUTH_CERT_OWNER_NAME = (By.ID, u'add_auth_cert_owner_name') # x: 870 y: 377 width: 313 height: 33, tag: p, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    OWNER_CLASS = (By.XPATH, u'//div[9]/div[2]/div[1]/section[1]/table[1]/tbody[1]/tr[2]/td[1]') # x: 735 y: 415 width: 130 height: 43, tag: td, type: , name: None, form_id: server_auth_cert_upload, checkbox: , table_id: 6, href:
    ID_ADD_AUTH_CERT_OWNER_CLASS = (By.ID, u'add_auth_cert_owner_class') # x: 870 y: 420 width: 313 height: 33, tag: p, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    OWNER = (By.XPATH, u'//div[9]/div[2]/div[1]/section[1]/table[1]/tbody[1]/tr[3]/td[1]') # x: 735 y: 458 width: 130 height: 43, tag: td, type: , name: None, form_id: server_auth_cert_upload, checkbox: , table_id: 6, href:
    ID_ADD_AUTH_CERT_OWNER_CODE = (By.ID, u'add_auth_cert_owner_code') # x: 870 y: 463 width: 313 height: 33, tag: p, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    SERVER = (By.XPATH, u'//div[9]/div[2]/div[1]/section[1]/table[1]/tbody[1]/tr[4]/td[1]') # x: 735 y: 501 width: 130 height: 43, tag: td, type: , name: None, form_id: server_auth_cert_upload, checkbox: , table_id: 6, href:
    ID_ADD_AUTH_CERT_SERVERCODE = (By.ID, u'add_auth_cert_servercode') # x: 870 y: 506 width: 313 height: 33, tag: p, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    AUTHENTICATION_CERTIFICATE_INFORMATION = (By.XPATH, u'//div[9]/div[2]/div[1]/section[2]/legend[1]') # x: 735 y: 564 width: 451 height: 30, tag: legend, type: , name: None, form_id: server_auth_cert_upload, checkbox: , table_id: 6, href:
    BUTTON_CANCEL = (By.XPATH, u'//div[9]/div[3]/div[1]/button[2]') # x: 1044 y: 658 width: 75 height: 37, tag: button, type: button, name: cancel, form_id: server_auth_cert_upload, checkbox: , table_id: 6, href:
    BUTTON_SUBMIT = (By.ID, u'auth_cert_add_submit') # x: 1129 y: 658 width: 76 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: , href:

    # Dynamic objects:
    ID_SECURITYSERVER_AUTH_CERT_UPLOAD_BUTTON = (By.ID, u'securityserver_auth_cert_upload_button')     # x: 735 y: 598 width: 83 height: 33 # Dynamic object
    MENUBAR_CLOSE = (By.XPATH, u'//div[10]/div[3]/div[1]/button[1]') # x: 1130 y: 765 width: 75 height: 36, tag: button, type: button, name: None, form_id: , checkbox: , table_id: , href: # Dynamic object

    def click_button_id_auth_cert_add_submit(self):
        """
        Click button to submit authentication certificate
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_SUBMIT*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # AutoGen method
        self.click_element(self.BUTTON_SUBMIT)
        self.wait_until_jquery_ajax_loaded()

    def click_upload_auth_cert(self):
        """
        Click button to upload authentication certificate
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_SECURITYSERVER_AUTH_CERT_UPLOAD_BUTTON*
        """
        self.click_element(self.ID_SECURITYSERVER_AUTH_CERT_UPLOAD_BUTTON)

    def click_element_submit(self):
        """
        Click button to close the dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.MENUBAR_CLOSE*
        """
        self.click_element(self.MENUBAR_CLOSE)
