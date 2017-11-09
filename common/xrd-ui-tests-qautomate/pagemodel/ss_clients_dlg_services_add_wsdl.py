# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_clients_dlg_services_add_wsdl(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20151209141405
    # Pagemodel url: https://dev-ss1.palveluvayla.com:4000/clients
    # Pagemodel area: (710, 402, 500, 167)
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
    MENUBAR_MAXIMIZE = (By.CSS_SELECTOR, u'div[data-name="wsdl_add_dialog"]>.ui-draggable-handle>.dialog-buttonbar>.ui-action-maximize') # x: 1108 y: 403 width: 51 height: 49
    MENUBAR_CLOSE = (By.CSS_SELECTOR, u'div[data-name="wsdl_add_dialog"]>.ui-draggable-handle>.dialog-buttonbar>.ui-action-close') # x: 1159 y: 403 width: 51 height: 49
    TITLE = (By.ID, u'ui-id-22') # x: 720 y: 418 width: 72 height: 21
    MENUBAR_MAXIMIZE_2 = (By.CSS_SELECTOR, u'div[data-name="wsdl_add_dialog"]>.ui-draggable-handle>.dialog-buttonbar>.ui-action-maximize>.fa-rotate-45') # x: 1124 y: 418 width: 21 height: 21
    ID_WSDL_ADD_URL = (By.ID, u'wsdl_add_url') # x: 814 y: 474 width: 351 height: 33
    BUTTON_CANCEL = (By.CSS_SELECTOR, u'div[data-name="wsdl_add_dialog"]>.ui-dialog-buttonpane>.ui-dialog-buttonset>button[data-name="cancel"]') # x: 1073 y: 524 width: 77 height: 37
    BUTTON_OK = (By.CSS_SELECTOR, u'div[data-name="wsdl_add_dialog"]>.ui-dialog-buttonpane>.ui-dialog-buttonset>button[data-name="ok"]') # x: 1160 y: 524 width: 45 height: 37

    def verify_add_wsdl_dlg_open(self):
        """
        Verify dialog is open

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.MENUBAR_MAXIMIZE_2*
        """
        self.wait_until_element_is_visible(self.MENUBAR_MAXIMIZE_2)

    def add_wsdl(self, parameters=None):
        """
        Input text to wsdl url field with parameters 'wsdl_add_url' and click button to ok
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_WSDL_ADD_URL*, *parameters[u'wsdl_add_url']*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
        """
        self.input_text(self.ID_WSDL_ADD_URL, parameters[u'wsdl_add_url'])
        self.click_element(self.BUTTON_OK)