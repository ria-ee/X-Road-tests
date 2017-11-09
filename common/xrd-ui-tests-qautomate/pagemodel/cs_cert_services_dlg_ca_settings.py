# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_cert_services_dlg_ca_settings(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20161007113724
    # Pagemodel url: https://test-cs2.i.palveluvayla.com:4000/approved_cas
    # Pagemodel area: (558, 307, 803, 357)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[8]/div[1]/div[1]/button[1]') # x: 1258 y: 311 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 3, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[8]/div[1]/div[1]/button[2]') # x: 1309 y: 311 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 3, href:
    TITLE = (By.ID, u'ui-id-4') # x: 570 y: 325 width: 80 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    THIS_CA_CAN_ONLY_BE_USED_FOR_TLS_AUTHENTICATION_MARK = (By.XPATH, u'//div[8]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[1]') # x: 575 y: 376 width: 333 height: 52, tag: td, type: , name: None, form_id: , checkbox: , table_id: 3, href:
    AUTHENTICATION_ONLY_ON_CHECKBOX = (By.XPATH, u'//div[8]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[2]/input[1]') # x: 913 y: 395 width: 13 height: 13, tag: input, type: checkbox, name: authentication_only, form_id: , checkbox: , table_id: 3, href:
    CERTIFICATE_PROFILE_INFO_FULLY_QUALIFIED_CLASS_NAME_THAT_IMPLEMENTS_THE = (By.XPATH, u'//div[8]/div[2]/div[1]/table[1]/tbody[1]/tr[2]/td[1]') # x: 575 y: 428 width: 333 height: 94, tag: td, type: , name: None, form_id: , checkbox: , table_id: 3, href:
    CERT_PROFILE_INFO_TEXT = (By.XPATH, u'//div[1]/table[1]/tbody[1]/tr[2]/td[2]/input[1]') # x: 913 y: 459 width: 429 height: 33, tag: input, type: text, name: cert_profile_info, form_id: , checkbox: , table_id: 3, href:
    MESSAGE_FA_TIMES = (By.CSS_SELECTOR, u'.message>.fa-times') # x: 1330 y: 589 width: 20 height: 19, tag: i, type: , name: None, form_id: , checkbox: , table_id: , href:
    BUTTON_CANCEL = (By.XPATH, u'//div[4]/div[1]/button[2]') # x: 1223 y: 619 width: 77 height: 37, tag: button, type: button, name: cancel, form_id: , checkbox: , table_id: 3, href:
    BUTTON_OK = (By.ID, u'ca_settings_submit') # x: 1310 y: 619 width: 45 height: 37, tag: button, type: button, name: ok, form_id: , checkbox: , table_id: , href:

    def input_text_to_cert_profile_info_text(self, parameters=None):
        """
        Input cerificate profile text

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.CERT_PROFILE_INFO_TEXT*, *parameters['name_extractor_method']*
        """
        # AutoGen method
        self.input_text(self.CERT_PROFILE_INFO_TEXT, parameters['name_extractor_method'])

    def click_button_id_ca_settings_submit(self):
        """
        Click submit button
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
        """
        # AutoGen method
        self.click_element(self.BUTTON_OK)