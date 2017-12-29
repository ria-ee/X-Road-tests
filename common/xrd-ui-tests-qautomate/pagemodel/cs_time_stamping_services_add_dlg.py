# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_time_stamping_services_add_dlg(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160801133639
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/tsps
    # Pagemodel area: (556, 360, 807, 252)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[1]') # x: 1258 y: 361 width: 51 height: 49, tag: button, type: submit, name: None, form_id: upload_tsp_cert, checkbox: , table_id: 3, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[2]') # x: 1309 y: 361 width: 51 height: 49, tag: button, type: submit, name: None, form_id: upload_tsp_cert, checkbox: , table_id: 3, href:
    TITLE = (By.ID, u'ui-id-3') # x: 570 y: 375 width: 187 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    URL = (By.XPATH, u'//div[7]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[1]') # x: 575 y: 426 width: 80 height: 43, tag: td, type: , name: None, form_id: upload_tsp_cert, checkbox: , table_id: 3, href:
    INPUT_TSP_URL = (By.ID, u'tsp_url') # x: 659 y: 431 width: 683 height: 33, tag: input, type: text, name: tsp_url, form_id: , checkbox: , table_id: 3, href:
    CERTIFICATE = (By.CSS_SELECTOR, u'.label') # x: 575 y: 469 width: 80 height: 31, tag: td, type: , name: None, form_id: , checkbox: , table_id: 3, href:
    BUTTON_CANCEL = (By.XPATH, u'//div[7]/div[3]/div[1]/button[2]') # x: 1223 y: 569 width: 77 height: 37, tag: button, type: button, name: None, form_id: upload_tsp_cert, checkbox: , table_id: 3, href:
    BUTTON_OK = (By.ID, u'tsp_url_and_cert_submit') # x: 1310 y: 569 width: 45 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: , href:

    # Dynamic objects:
    BUTTON_UPLOAD = (By.ID, u'tsp_cert_button') # x: 1259 y: 468 width: 81 height: 33, tag: label, type: , name: None, form_id: , checkbox: , table_id: , href: # Dynamic object

    def input_text_to_id_tsp_url(self, parameters=None):
        """
        Input text to timestamping url field using parameter 'tsp_url'

        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.input_text`, *self.INPUT_TSP_URL*, *parameters['tsp_url']*
        """
        # AutoGen method
        self.input_text(self.INPUT_TSP_URL, parameters['tsp_url'])

    def click_button_ok(self):
        """
        Click button to ok the dialog
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
        """
        # AutoGen method
        self.click_element(self.BUTTON_OK)

    def click_button_upload(self):
        """
        Click button to upload timestamping

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_UPLOAD*
        """
        self.click_element(self.BUTTON_UPLOAD)
