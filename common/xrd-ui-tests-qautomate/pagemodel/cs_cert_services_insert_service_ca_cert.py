# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_cert_services_insert_service_ca_cert(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160801132654
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/approved_cas
    # Pagemodel area: (659, 384, 604, 203)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[1]') # x: 1158 y: 386 width: 51 height: 49, tag: button, type: submit, name: None, form_id: upload_top_ca_cert, checkbox: , table_id: 3, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[2]') # x: 1209 y: 386 width: 51 height: 49, tag: button, type: submit, name: None, form_id: upload_top_ca_cert, checkbox: , table_id: 3, href:
    TITLE = (By.ID, u'ui-id-3') # x: 670 y: 400 width: 196 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    ID_CA_CERT_FILE = (By.ID, u'ca_cert_file') # x: 680 y: 456 width: 470 height: 33, tag: input, type: text, name: ca_cert_file, form_id: , checkbox: , table_id: 3, href:
    BUTTON_CANCEL = (By.XPATH, u'//div[7]/div[3]/div[1]/button[2]') # x: 1108 y: 544 width: 77 height: 37, tag: button, type: button, name: cancel, form_id: upload_top_ca_cert, checkbox: , table_id: 3, href:
    BUTTON_NEXT = (By.ID, u'ca_cert_submit') # x: 1195 y: 544 width: 60 height: 37, tag: button, type: button, name: ok, form_id: , checkbox: , table_id: , href:

    # Dynamic objects:
    BUTTON_BROWSE = (By.ID, u'ca_cert_button') # x: 1158 y: 456 width: 83 height: 33, tag: label, type: , name: None, form_id: , checkbox: , table_id: , href: # Dynamic object

    def click_button_browse(self):
        """
        Click browse button

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_BROWSE*
        """
        self.click_element(self.BUTTON_BROWSE)

    def click_button_next(self):
        """
        Click button next

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_NEXT*
        """
        self.click_element(self.BUTTON_NEXT)
