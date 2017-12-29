# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_cert_services_ocsp_add_new_dlg(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160830145351
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/approved_cas
    # Pagemodel area: (558, 358, 807, 256)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[10]/div[1]/div[1]/button[1]') # x: 1258 y: 361 width: 51 height: 49, tag: button, type: submit, name: None, form_id: upload_ocsp_responder_cert, checkbox: , table_id: 5, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[10]/div[1]/div[1]/button[2]') # x: 1309 y: 361 width: 51 height: 49, tag: button, type: submit, name: None, form_id: upload_ocsp_responder_cert, checkbox: , table_id: 5, href:
    TITLE = (By.ID, u'ui-id-10') # x: 570 y: 375 width: 150 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    URL_0 = (By.XPATH, u'//div[10]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[1]') # x: 575 y: 426 width: 80 height: 43, tag: td, type: , name: None, form_id: upload_ocsp_responder_cert, checkbox: , table_id: 5, href:
    ID_OCSP_RESPONDER_URL = (By.ID, u'ocsp_responder_url') # x: 659 y: 431 width: 683 height: 33, tag: input, type: text, name: ocsp_responder_url, form_id: , checkbox: , table_id: 5, href:
    CERTIFICATE = (By.XPATH, u'//div[10]/div[2]/div[1]/table[1]/tbody[1]/tr[2]/td[1]') # x: 575 y: 469 width: 80 height: 31, tag: td, type: , name: None, form_id: upload_ocsp_responder_cert, checkbox: , table_id: 5, href:
    BUTTON_CANCEL = (By.XPATH, u'//div[10]/div[3]/div[1]/button[2]') # x: 1223 y: 569 width: 77 height: 37, tag: button, type: button, name: cancel, form_id: upload_ocsp_responder_cert, checkbox: , table_id: 5, href:
    BUTTON_OK = (By.ID, u'ocsp_responder_url_and_cert_submit') # x: 1310 y: 569 width: 45 height: 37, tag: button, type: button, name: ok, form_id: , checkbox: , table_id: , href:

    def input_text_to_id_ocsp_responder_url(self, parameters=None):
        """
        Input oscp responder url value

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.ID_OCSP_RESPONDER_URL*, *parameters['ocsp_responder_url']*
        """
        # AutoGen method
        self.input_text(self.ID_OCSP_RESPONDER_URL, parameters['ocsp_responder_url'])

    def click_button_ok(self):
        """
        Click ok button
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
        """
        # AutoGen method
        self.click_element(self.BUTTON_OK)
