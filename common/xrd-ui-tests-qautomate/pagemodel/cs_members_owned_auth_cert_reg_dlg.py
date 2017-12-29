# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_members_owned_auth_cert_reg_dlg(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160426093155
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/
    # Pagemodel area: (707, 277, 503, 417)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[23]/div[1]/div[2]/button[1]') # x: 1108 y: 277 width: 51 height: 49, tag: button, type: submit, name: None, form_id: member_auth_cert_upload, checkbox: , table_id: 6, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[2]/button[2]') # x: 1159 y: 277 width: 51 height: 49, tag: button, type: submit, name: None, form_id: member_auth_cert_upload, checkbox: , table_id: 6, href:
    TITLE = (By.ID, u'ui-id-42') # x: 720 y: 292 width: 272 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    SECURITY_SERVER_INFORMATION = (By.XPATH, u'//div[23]/div[2]/div[1]/section[1]/h2[1]/span[1]') # x: 735 y: 350 width: 244 height: 22, tag: span, type: , name: None, form_id: member_auth_cert_upload, checkbox: , table_id: 6, href: None
    OWNER_NAME = (By.XPATH, u'//div[23]/div[2]/div[1]/section[1]/table[1]/tbody[1]/tr[1]/td[1]') # x: 735 y: 379 width: 130 height: 43, tag: td, type: , name: None, form_id: member_auth_cert_upload, checkbox: , table_id: 6, href:
    ID_OWNED_SERVER_OWNER_NAME = (By.ID, u'owned_server_owner_name') # x: 870 y: 384 width: 313 height: 33, tag: p, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    OWNER_CLASS = (By.XPATH, u'//div[23]/div[2]/div[1]/section[1]/table[1]/tbody[1]/tr[2]/td[1]') # x: 735 y: 422 width: 130 height: 43, tag: td, type: , name: None, form_id: member_auth_cert_upload, checkbox: , table_id: 6, href:
    ID_OWNED_SERVER_OWNER_CLASS = (By.ID, u'owned_server_owner_class') # x: 870 y: 427 width: 313 height: 33, tag: p, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    OWNER = (By.XPATH, u'//div[23]/div[2]/div[1]/section[1]/table[1]/tbody[1]/tr[3]/td[1]') # x: 735 y: 465 width: 130 height: 43, tag: td, type: , name: None, form_id: member_auth_cert_upload, checkbox: , table_id: 6, href:
    ID_OWNED_SERVER_OWNER_CODE = (By.ID, u'owned_server_owner_code') # x: 870 y: 470 width: 313 height: 33, tag: p, type: , name: None, form_id: , checkbox: , table_id: 5, href:
    SERVER = (By.XPATH, u'//div[23]/div[2]/div[1]/section[1]/table[1]/tbody[1]/tr[4]/td[1]') # x: 735 y: 508 width: 130 height: 43, tag: td, type: , name: None, form_id: member_auth_cert_upload, checkbox: , table_id: 6, href:
    ID_OWNED_SERVER_ADD_SERVERCODE = (By.ID, u'owned_server_add_servercode') # x: 870 y: 513 width: 313 height: 33, tag: input, type: text, name: None, form_id: , checkbox: , table_id: 5, href:
    AUTHENTICATION_CERTIFICATE_INFORMATION = (By.XPATH, u'//div[23]/div[2]/div[1]/section[2]/h2[1]/span[1]') # x: 735 y: 568 width: 342 height: 22, tag: span, type: , name: None, form_id: member_auth_cert_upload, checkbox: , table_id: 6, href: None
    BUTTON_CANCEL = (By.XPATH, u'//div[23]/div[3]/div[1]/button[2]') # x: 1042 y: 650 width: 77 height: 37, tag: button, type: button, name: None, form_id: member_auth_cert_upload, checkbox: , table_id: 6, href:
    BUTTON_SUBMIT = (By.ID, u'add_owned_server_submit') # x: 1129 y: 650 width: 76 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: , href:

    # Dynamic objects:
    ID_OWNED_SERVER_CERT_UPLOAD_BUTTON = (By.ID, u'owned_server_cert_upload_button') # x: 735 y: 591 width: 81 height: 33, tag: label, type: , name: None, form_id: , checkbox: , table_id: , href: # Dynamic object

    def input_text_to_id_owned_server_add_servercode(self, parameters=None):
        """
        Inpurt text to add owned server. Uses parameter 'security_server_code'

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_OWNED_SERVER_ADD_SERVERCODE*, *parameters['security_server_code']*
        """
        # AutoGen method
        self.input_text(self.ID_OWNED_SERVER_ADD_SERVERCODE, parameters['security_server_code'])

    def click_button_id_add_owned_server_submit(self):
        """
        Click button to submit dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_SUBMIT*
        """
        # AutoGen method
        self.click_element(self.BUTTON_SUBMIT)

    def click_element_id_owned_server_cert_upload_button(self):
        """
        Click button to upload certificate

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_OWNED_SERVER_CERT_UPLOAD_BUTTON*
        """
        self.click_element(self.ID_OWNED_SERVER_CERT_UPLOAD_BUTTON)
