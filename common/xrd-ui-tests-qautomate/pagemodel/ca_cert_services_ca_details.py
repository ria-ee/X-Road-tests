# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ca_cert_services_ca_details(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20161007172134
    # Pagemodel url: https://test-cs2.i.palveluvayla.com:4000/approved_cas
    # Pagemodel area: (484, 260, 952, 453)
    # Pagemodel screen resolution: (1920, 1080)
    # Use project settings: True
    # Used filters: id, css_selector, class_name, link_text, xpath
    # Xpath type: xpath-position
    # Depth of css path: 3
    # Minimize css selector: True
    # Create automated methods: True
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[9]/div[1]/div[1]/button[1]') # x: 1333 y: 261 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 3, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[9]/div[1]/div[1]/button[2]') # x: 1384 y: 261 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 3, href:
    TITLE = (By.ID, u'ui-id-5') # x: 495 y: 275 width: 217 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    CA_CERTIFICATE = (By.ID, u'ui-id-6') # x: 714 y: 327 width: 112 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/approved_cas#top_ca_cert_tab
    CA_SETTINGS = (By.ID, u'ui-id-7') # x: 827 y: 327 width: 97 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/approved_cas#ca_settings_tab
    OCSP_RESPONDERS = (By.ID, u'ui-id-8') # x: 925 y: 327 width: 143 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/approved_cas#ocsp_responders_tab
    INTERMEDIATE_CAS = (By.ID, u'ui-id-9') # x: 1068 y: 327 width: 138 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://test-cs2.i.palveluvayla.com:4000/approved_cas#intermediate_cas_tab
    SUBJECT_DISTINGUISHED_NAME = (By.XPATH, u'//div[9]/div[2]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]') # x: 500 y: 372 width: 202 height: 43, tag: td, type: , name: None, form_id: , checkbox: , table_id: 3, href:
    ID_TOP_CA_CERT_SUBJECT_DN = (By.ID, u'top_ca_cert_subject_dn') # x: 707 y: 377 width: 711 height: 33, tag: p, type: , name: None, form_id: , checkbox: , table_id: 3, href:
    ISSUER_DISTINGUISHED_NAME = (By.XPATH, u'//div[9]/div[2]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[2]/td[1]') # x: 500 y: 415 width: 202 height: 43, tag: td, type: , name: None, form_id: , checkbox: , table_id: 3, href:
    ID_TOP_CA_CERT_ISSUER_DN = (By.ID, u'top_ca_cert_issuer_dn') # x: 707 y: 420 width: 711 height: 33, tag: p, type: , name: None, form_id: , checkbox: , table_id: 3, href:
    VALID_FROM = (By.XPATH, u'//div[9]/div[2]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[3]/td[1]') # x: 500 y: 458 width: 202 height: 43, tag: td, type: , name: None, form_id: , checkbox: , table_id: 3, href:
    ID_TOP_CA_CERT_VALID_FROM = (By.ID, u'top_ca_cert_valid_from') # x: 707 y: 463 width: 711 height: 33, tag: p, type: , name: None, form_id: , checkbox: , table_id: 3, href:
    VALID_TO = (By.XPATH, u'//div[9]/div[2]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[4]/td[1]') # x: 500 y: 501 width: 202 height: 43, tag: td, type: , name: None, form_id: , checkbox: , table_id: 3, href:
    ID_TOP_CA_CERT_VALID_TO = (By.ID, u'top_ca_cert_valid_to') # x: 707 y: 506 width: 711 height: 33, tag: p, type: , name: None, form_id: , checkbox: , table_id: 3, href:
    ID_TOP_CA_CERT_VIEW = (By.ID, u'top_ca_cert_view') # x: 1268 y: 549 width: 148 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 3, href:
    BUTTON_CLOSE = (By.XPATH, u'//div[9]/div[3]/div[1]/button[1]') # x: 1363 y: 669 width: 67 height: 37, tag: button, type: button, name: close, form_id: , checkbox: , table_id: 3, href:

    def click_oscp_responders(self):
        """
        Click oscp responder tab

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.OCSP_RESPONDERS*
        """
        self.click_element(self.OCSP_RESPONDERS)

    def click_button_close(self):
        """
        Click close button

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_CLOSE*
        """
        self.click_element(self.BUTTON_CLOSE)
