# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_sec_servers_mgm_request_app_conf(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20151214094221
    # Pagemodel url: https://dev-cs.palveluvayla.com:4000/securityservers#
    # Pagemodel area: (800, 409, 501, 153)
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
    UI_ACTION_MAXIMIZE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-maximize') # x: 1197 y: 410 width: 51 height: 49
    UI_ACTION_CLOSE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-close') # x: 1248 y: 410 width: 51 height: 49
    TITLE = (By.ID, u'ui-id-17') # x: 809 y: 424 width: 162 height: 21
    DIALOG_CONTENT = (By.CSS_SELECTOR, u'div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-dialog-buttons.ui-draggable.ui-resizable>#confirm') # x: 799 y: 461 width: 500 height: 52
    BUTTON_CANCEL = (By.CSS_SELECTOR, u'button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only') # x: 1120 y: 518 width: 77 height: 37
    BUTTON_CONFIRM = (By.CSS_SELECTOR, u'div.ui-dialog-buttonset>#confirm') # x: 1207 y: 518 width: 87 height: 37

    def click_confirm_approve_request(self):
        """
        Click confirm to approve request
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_CONFIRM*
        """
        self.click_element(self.BUTTON_CONFIRM)