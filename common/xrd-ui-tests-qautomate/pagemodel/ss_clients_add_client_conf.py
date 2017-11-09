# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_clients_add_client_conf(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20151214092739
    # Pagemodel url: https://dev-ss1.palveluvayla.com:4000/clients
    # Pagemodel area: (720, 408, 503, 152)
    # Pagemodel screen resolution: (1920, 1080)
    # Use project settings: True
    # Used filters: id, css_selector, class_name, link_text, xpath
    # Depth of css path: 8
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
    UI_ACTION_MAXIMIZE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-maximize') # x: 1119 y: 410 width: 51 height: 49
    UI_ACTION_CLOSE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-close') # x: 1170 y: 410 width: 51 height: 49
    TITLE = (By.ID, u'ui-id-33') # x: 731 y: 424 width: 162 height: 21
    BUTTON_CONFRIM = (By.CSS_SELECTOR, u'div.ui-dialog-buttonset>#confirm') # x: 1128 y: 518 width: 87 height: 37

    def click_confirm_client_registration_request(self):
        """
        Click button to confirm client registeration

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_CONFRIM*
        """
        self.click_element(self.BUTTON_CONFRIM)