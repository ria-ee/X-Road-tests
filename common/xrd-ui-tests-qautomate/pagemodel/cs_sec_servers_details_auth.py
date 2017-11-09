# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_sec_servers_details_auth(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160301120157
    # Pagemodel url: https://dev-cs.palveluvayla.com:4000/securityservers
    # Pagemodel area: (460, 183, 1010, 606)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[1]') # x: 1358 y: 183 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: securityserver_auth_certs, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[2]') # x: 1409 y: 183 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: securityserver_auth_certs, href:
    ID_SECURITYSERVER_AUTHCERT_ADD = (By.ID, u'securityserver_authcert_add') # x: 1213 y: 192 width: 54 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_SECURITYSERVER_AUTHCERT_DELETE = (By.ID, u'securityserver_authcert_delete') # x: 1271 y: 192 width: 73 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    TITLE = (By.ID, u'ui-id-3') # x: 470 y: 198 width: 157 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    SECURITY_SERVER_DETAILS = (By.ID, u'ui-id-4') # x: 652 y: 250 width: 172 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://dev-cs.palveluvayla.com:4000/securityservers#server_details_tab
    CLIENTS = (By.ID, u'ui-id-5') # x: 825 y: 250 width: 66 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://dev-cs.palveluvayla.com:4000/securityservers#server_clients_tab
    AUTHENTICATION_CERTIFICATES = (By.ID, u'ui-id-6') # x: 892 y: 250 width: 200 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://dev-cs.palveluvayla.com:4000/securityservers#server_auth_certs_tab
    MANAGEMENT_REQUESTS = (By.ID, u'ui-id-7') # x: 1093 y: 250 width: 176 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://dev-cs.palveluvayla.com:4000/securityservers#server_management_requests_tab
    CA = (By.XPATH, u'//div[3]/section[1]/div[1]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 486 y: 305 width: 237 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: securityserver_auth_certs, href:
    SERIAL_NUMBER = (By.XPATH, u'//div[3]/section[1]/div[1]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[2]') # x: 723 y: 305 width: 237 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: securityserver_auth_certs, href:
    SUBJECT = (By.XPATH, u'//div[3]/section[1]/div[1]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[3]') # x: 960 y: 305 width: 237 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: securityserver_auth_certs, href:
    EXPIRES = (By.XPATH, u'//div[3]/section[1]/div[1]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[4]') # x: 1197 y: 305 width: 237 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: securityserver_auth_certs, href:
    BUTTON_CLOSE = (By.XPATH, u'//div[7]/div[3]/div[1]/button[1]') # x: 1390 y: 741 width: 65 height: 37, tag: button, type: button, name: close, form_id: , checkbox: , table_id: securityserver_auth_certs, href:

    def click_button_id_securityserver_authcert_add(self):
        """
        Click button to add authentication certificate
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_SECURITYSERVER_AUTHCERT_ADD*
        """
        # AutoGen method
        self.click_element(self.ID_SECURITYSERVER_AUTHCERT_ADD)

    def click_button_id_securityserver_authcert_delete(self):
        """
        Click button to delete authentication certificate
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_SECURITYSERVER_AUTHCERT_DELETE*
        """
        # AutoGen method
        self.click_element(self.ID_SECURITYSERVER_AUTHCERT_DELETE)

    def click_element_from_table_securityserver_auth_certs(self, text=u'Xroad Test CA'):
        """
        Click security server authentication in security server authentications table with given text
        
        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *element*
        """
        self.wait_until_jquery_ajax_loaded()

        # Element search
        locator =  (By.ID, u'securityserver_auth_certs')
        value = text
        row = u'TBODY/TR'
        cell = u'TD'
        element_info = self.get_table_column_and_row_by_text(locator, value, row, cell)

        # Searched element info
        row_number = element_info[2]
        column_number = element_info[3]
        row_element = element_info[0]
        element = element_info[1]

        # Action for the element
        self.click_element(element)
