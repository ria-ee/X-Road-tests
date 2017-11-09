# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_sec_servers_details(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20151215134503
    # Pagemodel url: https://dev-cs.palveluvayla.com:4000/securityservers
    # Pagemodel area: (459, 183, 1001, 603)
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
    # Links found: 0
    # Page model constants:
    UI_ACTION_MAXIMIZE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-maximize') # x: 1358 y: 185 width: 51 height: 49
    UI_ACTION_CLOSE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-close') # x: 1409 y: 185 width: 51 height: 49
    ID_SECURITYSERVER_DELETE = (By.ID, u'securityserver_delete') # x: 1270 y: 193 width: 74 height: 33
    TITLE = (By.ID, u'ui-id-3') # x: 470 y: 199 width: 159 height: 21
    SECURITY_SERVER_DETAILS = (By.ID, u'ui-id-4') # x: 650 y: 251 width: 173 height: 29
    CLIENTS = (By.LINK_TEXT, u'Clients') # x: 824 y: 251 width: 66 height: 29
    AUTHENTICATION_CERTIFICATES = (By.XPATH, u'//*[@href=\'#server_auth_certs_tab\']')  # x: 718 y: 194 width: 201 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://xroad-lxd-cs.lxd:4000/#server_auth_certs_tab
    MANAGEMENT_REQUESTS = (By.XPATH, u'//*[@href=\'#server_management_requests_tab\']')  # x: 920 y: 194 width: 177 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://xroad-lxd-cs.lxd:4000/#server_management_requests_tab
    ID_SECURITYSERVER_EDIT_TABLE = (By.ID, u'securityserver_edit_table') # x: 485 y: 306 width: 951 height: 258
    BUTTON_CLOSE = (By.CSS_SELECTOR, u'div.ui-dialog-buttonset>button[data-name="close"]') # x: 1388 y: 743 width: 67 height: 37

    # Dynamic objects:
    HREFSERVER_CLIENTS_TAB = (By.XPATH, u'//*[@href=\'#server_clients_tab\']') # x: 651 y: 194 width: 66 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://xroad-lxd-cs.lxd:4000/#server_clients_tab
    CLASS_MESSAGE = (By.CLASS_NAME, u'message')     # x: 460 y: 706 width: 1000 height: 30 # Dynamic object

    def verify_ss_details_view(self):
        """
        Verify that page contains security server edit table

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.ID_SECURITYSERVER_EDIT_TABLE*
        """
        self.wait_until_element_is_visible(self.ID_SECURITYSERVER_EDIT_TABLE)

    def click_clients_tab(self):
        """
        Click tab to show clients view in dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.CLIENTS*
        """
        self.click_element(self.CLIENTS)

    def click_mgm_requests_tab(self):
        """
        Click tab to show management request view in dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.MANAGEMENT_REQUESTS*
        """
        self.click_element(self.MANAGEMENT_REQUESTS)

    def click_authentication_certificates_tab(self):
        """
        Click tab to show auhtentication certificates view in dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.AUTHENTICATION_CERTIFICATES*
        """
        self.click_element(self.AUTHENTICATION_CERTIFICATES)

    def wait_until_submitted_certificate(self):
        """
        Wait until message shows that certificate has been submitted. Massage u'Request of adding auth'

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_contains`, *self.CLASS_MESSAGE*, *u'Request of adding auth'*
        """
        self.wait_until_element_contains(self.CLASS_MESSAGE, u'Request of adding auth')

    def click_element_id_securityserver_delete(self):
        """
        Click button to delete security server

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_SECURITYSERVER_DELETE*
        """
        self.click_element(self.ID_SECURITYSERVER_DELETE)

    def click_security_server_details_tab(self):
        """
        Click tab to show security server details view in dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.SECURITY_SERVER_DETAILS*
        """
        self.click_element(self.SECURITY_SERVER_DETAILS)
