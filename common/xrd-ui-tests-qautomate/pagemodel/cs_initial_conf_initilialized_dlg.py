# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_initial_conf_initilialized_dlg(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160802134245
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/init
    # Pagemodel area: (810, 410, 302, 152)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[1]') # x: 1008 y: 411 width: 51 height: 49, tag: button, type: submit, name: None, form_id: init, checkbox: , table_id: 2, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[2]') # x: 1059 y: 411 width: 51 height: 49, tag: button, type: submit, name: None, form_id: init, checkbox: , table_id: 2, href:
    TITLE = (By.ID, u'ui-id-3') # x: 820 y: 425 width: 46 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    ID_ALERT = (By.ID, u'alert') # x: 810 y: 462 width: 300 height: 52, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href:
    BUTTON_OK = (By.XPATH, u'//div[7]/div[3]/div[1]/button[1]') # x: 1060 y: 519 width: 45 height: 37, tag: button, type: button, name: None, form_id: init, checkbox: , table_id: 2, href:

    def click_button_ok(self):
        """
        Click button to ok the dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
        """
        # AutoGen method submit form: init
        self.click_element(self.BUTTON_OK)
