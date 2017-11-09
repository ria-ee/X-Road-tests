# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_clients_dlg_services_edit_wsdl(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20151210140009
    # Pagemodel url: https://dev-ss1.palveluvayla.com:4000/clients
    # Pagemodel area: (658, 339, 604, 292)
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
    # Row count: 25
    # Element count: 140
    # Big element filter width: 55
    # Big element filter height: 40
    # Not filtered elements: button, strong, select
    # Canvas modeling: False
    # Pagemodel type: normal
    # Links found: 0
    # Page model constants:
    MENUBAR_MAXIMIZE = (By.CSS_SELECTOR, u'div[data-name="service_params_dialog"]>.ui-draggable-handle>.dialog-buttonbar>.ui-action-maximize') # x: 1158 y: 341 width: 51 height: 49
    MENUBAR_CLOSE = (By.CSS_SELECTOR, u'div[data-name="service_params_dialog"]>.ui-draggable-handle>.dialog-buttonbar>.ui-action-close') # x: 1209 y: 341 width: 51 height: 49
    TITLE = (By.ID, u'ui-id-25') # x: 670 y: 355 width: 167 height: 21
    ID_PARAMS_URL = (By.ID, u'params_url') # x: 851 y: 452 width: 199 height: 33
    ID_PARAMS_URL_ALL = (By.ID, u'params_url_all') # x: 1138 y: 461 width: 13 height: 13
    ID_PARAMS_TIMEOUT = (By.ID, u'params_timeout') # x: 851 y: 495 width: 199 height: 33
    ID_PARAMS_TIMEOUT_ALL = (By.ID, u'params_timeout_all') # x: 1138 y: 504 width: 13 height: 13
    ID_PARAMS_SSLAUTH = (By.ID, u'params_sslauth') # x: 851 y: 541 width: 13 height: 13
    ID_PARAMS_SSLAUTH_ALL = (By.ID, u'params_sslauth_all') # x: 1138 y: 541 width: 13 height: 13
    BUTTON_CANCEL = (By.CSS_SELECTOR, u'div[data-name="service_params_dialog"]>.ui-dialog-buttonpane>.ui-dialog-buttonset>button[data-name="cancel"]') # x: 1123 y: 587 width: 77 height: 37
    BUTTON_OK = (By.CSS_SELECTOR, u'div[data-name="service_params_dialog"]>.ui-dialog-buttonpane>.ui-dialog-buttonset>button[data-name="ok"]') # x: 1210 y: 587 width: 45 height: 37

    def verify_edit_serv_param_dlg_open(self):
        """
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.MENUBAR_MAXIMIZE*
        """
        self.wait_until_element_is_visible(self.MENUBAR_MAXIMIZE)

    def fill_service_parameters(self, parameters=None):
        """

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_PARAMS_URL*, *changed_http_in_url*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.select_checkbox`, *self.ID_PARAMS_URL_ALL*, *parameters[u'params_url_all']*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_PARAMS_TIMEOUT*, *parameters[u'params_timeout']*
            * **Step 4:** :func:`~webframework.extension.util.common_utils.CommonUtils.select_checkbox`, *self.ID_PARAMS_SSLAUTH*, *parameters[u'params_sslauth']*
        """
        import string
        changed_https_in_url = ""
        try:
            changed_port_in_url = string.replace(parameters[u'params_url'], "4400", parameters[u'mgm_services_port'])
            changed_http_in_url = string.replace(changed_port_in_url, "http", parameters[u'mgm_services_protocol'])
        except:
            changed_http_in_url = parameters[u'params_url']
        self.input_text(self.ID_PARAMS_URL, changed_http_in_url)
        self.select_checkbox(self.ID_PARAMS_URL_ALL, parameters[u'params_url_all'])
        self.input_text(self.ID_PARAMS_TIMEOUT, parameters[u'params_timeout'])
        #self.select_checkbox(self.ID_PARAMS_TIMEOUT_ALL, parameters[u'params_timeout_all'])
        try:
            self.select_checkbox(self.ID_PARAMS_SSLAUTH, parameters[u'params_sslauth'])
        except:
            print("Could not set sslauth to checkin")
        #self.select_checkbox(self.ID_PARAMS_SSLAUTH_ALL, parameters[u'params_sslauth_all'])

    def click_ok_service_parameters(self):
        """
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
        """
        self.click_element(self.BUTTON_OK)
        sleep(1)

