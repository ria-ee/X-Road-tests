# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_cert_services(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160830144256
    # Pagemodel url: https://test-cs2.i.palveluvayla.com:4000/approved_cas
    # Pagemodel area: (272, 1, 1640, 621)
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
    ID_CA_DETAILS = (By.ID, u'ca_details') # x: 1540 y: 8 width: 54 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_CA_ADD = (By.ID, u'ca_add') # x: 1601 y: 8 width: 53 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_CA_DELETE = (By.ID, u'ca_delete') # x: 1661 y: 8 width: 74 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_HEADING = (By.ID, u'heading') # x: 290 y: 14 width: 190 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    CAS_FILTER_TEXT = (By.CSS_SELECTOR, u'#cas_filter>label>input') # x: 346 y: 76 width: 179 height: 33, tag: input, type: text, name: None, form_id: , checkbox: , table_id: , href:
    TRUSTED_CERTIFICATION_SERVICE = (By.XPATH, u'//div[2]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 291 y: 115 width: 1252 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: cas, href:
    VALID_FROM = (By.XPATH, u'//div[2]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[2]') # x: 1543 y: 115 width: 178 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: cas, href:
    VALID_TO = (By.XPATH, u'//div[2]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[3]') # x: 1721 y: 115 width: 178 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: cas, href:
    TRUSTED_CERT_FIRST_ROW = (By.XPATH, u'//div[2]/div[2]/table[1]/tbody[1]/tr[1]/td[1]') # x: 291 y: 153 width: 1252 height: 31, tag: td, type: , name: None, form_id: , checkbox: , table_id: cas, href:

    def click_button_id_ca_details(self):
        """
        Click details button

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_CA_DETAILS*
        """
        # AutoGen method
        self.click_element(self.ID_CA_DETAILS)

    def click_button_id_ca_add(self):
        """
        Click add ca button

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_CA_ADD*
        """
        # AutoGen method
        self.click_element(self.ID_CA_ADD)

    def click_trusted_cert_table_first_row(self):
        """
        Click certificates tables first row

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.TRUSTED_CERT_FIRST_ROW*
        """
        self.click_element(self.TRUSTED_CERT_FIRST_ROW)
