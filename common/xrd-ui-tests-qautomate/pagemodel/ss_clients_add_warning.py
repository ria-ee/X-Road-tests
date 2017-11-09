# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_clients_add_warning(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160510135743
    # Pagemodel url: https://test-rh1.i.palveluvayla.com:4000/clients
    # Pagemodel area: (661, 409, 597, 154)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[24]/div[1]/div[1]/button[1]') # x: 1155 y: 410 width: 51 height: 49, tag: button, type: submit, name: None, form_id: clients, checkbox: , table_id: 3, href: 
    MENUBAR_CLOSE = (By.XPATH, u'//div[24]/div[1]/div[1]/button[2]') # x: 1206 y: 410 width: 51 height: 49, tag: button, type: submit, name: None, form_id: clients, checkbox: , table_id: 3, href: 
    TITLE = (By.ID, u'ui-id-33') # x: 673 y: 424 width: 59 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    BUTTON_CANCEL = (By.XPATH, u'//div[24]/div[3]/div[1]/button[2]') # x: 1071 y: 518 width: 77 height: 37, tag: button, type: button, name: None, form_id: clients, checkbox: , table_id: 3, href: 

    # Dynamic objects:
    CONTINUE = (By.XPATH, u'//div[24]/div[3]/div[1]/button[1]') # x: 1158 y: 518 width: 95 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: , href: # Dynamic object

    def click_element_continue(self):
        """
        Click button to continue

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.CONTINUE*
        """
        self.click_element(self.CONTINUE)
