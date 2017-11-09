# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = self.get_current_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_backup_restore_confirm_delete(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20170322140931
    # Pagemodel url: https://xroad-lxd-ss2.lxd:4000/backup
    # Pagemodel area: Full screen
    # Pagemodel screen resolution: (1920, 1080)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[8]/div[1]/div[1]/button[1]') # x: 1248 y: 405 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: backup_files, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[8]/div[1]/div[1]/button[2]') # x: 1299 y: 405 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: backup_files, href:
    TITLE = (By.ID, u'ui-id-4') # x: 580 y: 420 width: 167 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    DIALOG_CONTENT = (By.CSS_SELECTOR, u'div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-dialog-buttons.ui-draggable.ui-resizable>#confirm') # x: 570 y: 456 width: 780 height: 53, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href:
    CANCEL = (By.XPATH, u'//div[11]/div[1]/button[2]') # x: 1175 y: 514 width: 75 height: 36, tag: button, type: button, name: None, form_id: , checkbox: , table_id: backup_files, href:
    BUTTON_CONFIRM = (By.CSS_SELECTOR, u'div.ui-dialog-buttonset>#confirm') # x: 1260 y: 514 width: 85 height: 36, tag: button, type: button, name: None, form_id: , checkbox: , table_id: , href:

    def click_button_confirm(self):
        """
        Click button to confirm the dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_CONFIRM*
        """
        self.click_element(self.BUTTON_CONFIRM)
