# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = self.get_current_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_version(CommonUtils):
    """

    """
    # Pagemodel timestamp: 20170927121424
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/about
    # Pagemodel area: (271, 1, 1563, 812)
    # Pagemodel screen resolution: (1920, 975)
    # Use project settings: True
    # Used filters: id, css_selector, class_name, link_text, xpath
    # Xpath type: xpath-position
    # Create automated methods: False
    # Depth of css path: 3
    # Minimize css selector: True
    # Use css pattern: False
    # Allow non unique css pattern: False
    # Pagemodel template: False
    # Use testability: True
    # testability attribute: data-name
    # Use contains text in xpath: False
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
    GROUP = (By.CSS_SELECTOR, u'.button-group') # x: 1818 y: 0 width: 21 height: 50, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href:
    ID_HEADING = (By.ID, u'heading') # x: 290 y: 14 width: 69 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    # Dynamic objects:
    VERSION_TEXT = (By.ID, u'content-inner') # x: 290 y: 70 width: 1610 height: 20, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href:

    def verify_version_text(self, text=u'Central Server version 6'):
        """
        Verify version text with text

        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_should_contain`, *self.VERSION_TEXT*, *text*
        """
        self.element_should_contain(self.VERSION_TEXT, text)
