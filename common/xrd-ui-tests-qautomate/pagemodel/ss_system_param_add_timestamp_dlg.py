# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_system_param_add_timestamp_dlg(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160414100022
    # Pagemodel url: https://test-ss1.i.palveluvayla.com:4000/sysparams
    # Pagemodel area: (660, 282, 601, 401)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[1]') # x: 1158 y: 283 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: tsps_approved, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[2]') # x: 1209 y: 283 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: tsps_approved, href:
    TITLE = (By.ID, u'ui-id-3') # x: 670 y: 298 width: 187 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    TRUSTED_TIMESTAMPING_SERVICES = (By.XPATH, u'//div[1]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 676 y: 350 width: 569 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: tsps_approved, href:
    TRUSTED_TSP_TABLE_FIRST_ROW = (By.XPATH, u'//div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[1]') # x: 676 y: 388 width: 569 height: 31, tag: td, type: , name: None, form_id: , checkbox: , table_id: tsps_approved, href:
    BUTTON_CANCEL = (By.XPATH, u'//div[7]/div[3]/div[1]/button[2]') # x: 1123 y: 641 width: 77 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: tsps_approved, href:
    BUTTON_OK = (By.XPATH, u'//div[7]/div[3]/div[1]/button[1]') # x: 1210 y: 641 width: 45 height: 37, tag: button, type: button, name: ok, form_id: , checkbox: , table_id: tsps_approved, href:

    def click_button_ok(self):
        """
        Click button to confrim dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
        """
        self.click_element(self.BUTTON_OK)

    def click_trusted_tsp_first_row(self):
        """
        Click timestamping tables first row

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.TRUSTED_TSP_TABLE_FIRST_ROW*
        """
        self.click_element(self.TRUSTED_TSP_TABLE_FIRST_ROW)
