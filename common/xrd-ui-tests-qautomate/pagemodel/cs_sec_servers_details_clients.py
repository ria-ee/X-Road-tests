# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_sec_servers_details_clients(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20151215140401
    # Pagemodel url: https://dev-cs.palveluvayla.com:4000/securityservers
    # Pagemodel area: (460, 185, 1001, 601)
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
    # Links found: 2
    # Page model constants:
    UI_ACTION_MAXIMIZE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-maximize') # x: 1358 y: 185 width: 51 height: 49
    UI_ACTION_CLOSE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-close') # x: 1409 y: 185 width: 51 height: 49
    ID_SECURITYSERVER_CLIENT_ADD = (By.ID, u'securityserver_client_add') # x: 1213 y: 193 width: 53 height: 33
    ID_SECURITYSERVER_CLIENT_DELETE = (By.ID, u'securityserver_client_delete') # x: 1270 y: 193 width: 74 height: 33
    SECURITY_SEVER_DETAILS = (By.ID, u'ui-id-3') # x: 470 y: 199 width: 159 height: 21
    SECURITY_SERVER_DETAILS = (By.ID, u'ui-id-4') # x: 650 y: 251 width: 173 height: 29
    CLIENTS = (By.ID, u'ui-id-5') # x: 824 y: 251 width: 66 height: 29
    AUTH_CERT = (By.ID, u'ui-id-6') # x: 891 y: 251 width: 201 height: 29
    MANAGEMENT_REQUESTS = (By.ID, u'ui-id-7') # x: 1093 y: 251 width: 177 height: 29
    SECURITYSERVER_CLIENTS_WRAPPER_DATA_TABLES_SCROLL_HEAD_INNER_SORTING_ASC = (By.CSS_SELECTOR, u'#securityserver_clients_wrapper>.dataTables_scroll>.dataTables_scrollHead>.dataTables_scrollHeadInner>.dataTable>thead>tr>.sorting_asc') # x: 486 y: 307 width: 237 height: 37
    ID_SECURITYSERVER_CLIENTS_WRAPPER_CLASS = (By.XPATH, u'id(\'securityserver_clients_wrapper\')/DIV[1]/DIV[1]/DIV[1]/TABLE[1]/THEAD[1]/TR[1]/TH[2]') # x: 723 y: 307 width: 237 height: 37
    ID_SECURITYSERVER_CLIENTS_WRAPPER = (By.XPATH, u'id(\'securityserver_clients_wrapper\')/DIV[1]/DIV[1]/DIV[1]/TABLE[1]/THEAD[1]/TR[1]/TH[3]') # x: 960 y: 307 width: 237 height: 37
    ID_SECURITYSERVER_CLIENTS_WRAPPER_SUBSYSTEM = (By.XPATH, u'id(\'securityserver_clients_wrapper\')/DIV[1]/DIV[1]/DIV[1]/TABLE[1]/THEAD[1]/TR[1]/TH[4]') # x: 1197 y: 307 width: 237 height: 37
    UI_BUTTONSET_DATA_NAME_CLOSE = (By.CSS_SELECTOR, u'div.ui-dialog-buttonset>button[data-name="close"]') # x: 1388 y: 743 width: 67 height: 37

    # Dynamic objects:
    SUBMIT = (By.XPATH, u'//div[7]/div[1]/div[1]/button[2]') # x: 1409 y: 180 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href: # Dynamic object

    def click_add_new_client_request(self):
        """
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_SECURITYSERVER_CLIENT_ADD*
        """
        self.click_element(self.ID_SECURITYSERVER_CLIENT_ADD)

    def search_text_from_table_securityserver_clients_1(self, parameters=None):
        """
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *element*
        """
        self.wait_until_jquery_ajax_loaded()

        # Element search
        locator = (By.ID, u'securityserver_clients')
        value = parameters[u'member_name']
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

    def click_element_id_securityserver_client_delete(self):
        """
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_SECURITYSERVER_CLIENT_DELETE*
        """
        self.click_element(self.ID_SECURITYSERVER_CLIENT_DELETE)

    def click_element_submit(self):
        """
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.SUBMIT*
        """
        self.click_element(self.SUBMIT)

    def click_element_auth_cert(self):
        """
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.AUTH_CERT*
        """
        self.click_element(self.AUTH_CERT)
