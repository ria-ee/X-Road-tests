# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_time_stamping_services(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160801133201
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/tsps
    # Pagemodel area: (272, 2, 1640, 562)
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
    ID_TSP_DETAILS = (By.ID, u'tsp_details') # x: 1540 y: 8 width: 54 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_TSP_ADD = (By.ID, u'tsp_add') # x: 1601 y: 8 width: 53 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_TSP_DELETE = (By.ID, u'tsp_delete') # x: 1661 y: 8 width: 74 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID_HEADING = (By.ID, u'heading') # x: 290 y: 14 width: 198 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    ID_RECORDS_COUNT = (By.ID, u'records_count') # x: 492 y: 14 width: 19 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    TSPS_FILTER_TEXT = (By.CSS_SELECTOR, u'#tsps_filter>label>input') # x: 346 y: 76 width: 179 height: 33, tag: input, type: text, name: None, form_id: , checkbox: , table_id: , href:
    NAME = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 291 y: 115 width: 1252 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: tsps, href:
    VALID_FROM = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[2]') # x: 1543 y: 115 width: 178 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: tsps, href:
    VALID_TO = (By.XPATH, u'//div[1]/table[1]/thead[1]/tr[1]/th[3]') # x: 1721 y: 115 width: 178 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: tsps, href:

    def click_button_id_tsp_add(self):
        """
        Click button to add timestamping
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_TSP_ADD*
        """
        # AutoGen method
        self.click_element(self.ID_TSP_ADD)