# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_remove_member_dlg(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160411121632
    # Pagemodel url: https://test-cs.i.palveluvayla.com:4000/
    # Pagemodel area: (589, 395, 503, 153)
    # Pagemodel screen resolution: (1680, 1050)
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
    MENUBAR_SUBMIT = (By.XPATH, u'//div[23]/div[1]/div[1]/button[1]') # x: 989 y: 395 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 3, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[23]/div[1]/div[1]/button[2]') # x: 1040 y: 395 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: 3, href:
    TITLE = (By.ID, u'ui-id-33') # x: 601 y: 409 width: 162 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    DIALOG_CONTENT = (By.CSS_SELECTOR, u'div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-dialog-buttons.ui-draggable.ui-resizable>#confirm') # x: 591 y: 446 width: 500 height: 52, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href:
    BUTTON_CANCEL = (By.XPATH, u'//div[23]/div[3]/div[1]/button[2]') # x: 912 y: 503 width: 77 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: 3, href:
    BUTTON_CONFIRM = (By.CSS_SELECTOR, u'div.ui-dialog-buttonset>#confirm') # x: 999 y: 503 width: 87 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: , href:

    def click_link_confirm_ui_text(self):
        """
        Click button to confirm the dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_CONFIRM*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        # AutoGen method click_link: None
        self.click_element(self.BUTTON_CONFIRM)
        self.wait_until_jquery_ajax_loaded()
