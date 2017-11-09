# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_cert_services_ocsp_responder_dlg(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160830144902
    # Pagemodel url: https://test-cs2.i.palveluvayla.com:4000/approved_cas
    # Pagemodel area: (482, 257, 960, 454)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[9]/div[1]/div[1]/button[1]') # x: 1333 y: 261 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: ocsp_responders, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[9]/div[1]/div[1]/button[2]') # x: 1384 y: 261 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: ocsp_responders, href:
    ID_OCSP_RESPONDER_EDIT = (By.ID, u'ocsp_responder_edit') # x: 1130 y: 269 width: 54 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_OCSP_RESPONDER_ADD = (By.ID, u'ocsp_responder_add') # x: 1187 y: 269 width: 53 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_OCSP_RESPONDER_DELETE = (By.ID, u'ocsp_responder_delete') # x: 1244 y: 269 width: 74 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    TITLE = (By.ID, u'ui-id-5') # x: 495 y: 275 width: 217 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    CA_CERTIFICATE = (By.ID, u'ui-id-6') # x: 714 y: 327 width: 112 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/approved_cas#top_ca_cert_tab
    CA_SETTINGS = (By.ID, u'ui-id-7') # x: 827 y: 327 width: 97 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/approved_cas#ca_settings_tab
    OCSP_RESPONDERS = (By.ID, u'ui-id-8') # x: 925 y: 327 width: 143 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/approved_cas#ocsp_responders_tab
    INTERMEDIATE_CAS = (By.ID, u'ui-id-9') # x: 1068 y: 327 width: 138 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/approved_cas#intermediate_cas_tab
    URL = (By.XPATH, u'//div[3]/div[1]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 501 y: 373 width: 753 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: ocsp_responders, href:
    BUTTON_CLOSE = (By.XPATH, u'//div[9]/div[3]/div[1]/button[1]') # x: 1363 y: 669 width: 67 height: 37, tag: button, type: button, name: close, form_id: , checkbox: , table_id: ocsp_responders, href:

    def click_button_id_ocsp_responder_add(self):
        """
        Click add button

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_OCSP_RESPONDER_ADD*
        """
        # AutoGen method
        self.click_element(self.ID_OCSP_RESPONDER_ADD)

    def click_button_close(self):
        """
        Click close button

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_CLOSE*
        """
        # AutoGen method
        self.click_element(self.BUTTON_CLOSE)