# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = self.get_current_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_backup_restore_confirm_restore(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20170322124803
    # Pagemodel url: https://xroad-lxd-ss2.lxd:4000/backup
    # Pagemodel area: (711, 405, 502, 150)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[8]/div[1]/div[1]/button[1]') # x: 1110 y: 405 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: backup_files, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[8]/div[1]/div[1]/button[2]') # x: 1161 y: 405 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: backup_files, href:
    TITLE = (By.ID, u'ui-id-4') # x: 718 y: 420 width: 167 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    DIALOG_CONTENT = (By.CSS_SELECTOR, u'div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-dialog-buttons.ui-draggable.ui-resizable>#confirm') # x: 708 y: 456 width: 504 height: 53, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href:
    BUTTON_CANCEL = (By.XPATH, u'//div[11]/div[1]/button[2]') # x: 1037 y: 514 width: 75 height: 36, tag: button, type: button, name: None, form_id: , checkbox: , table_id: backup_files, href:
    BUTTON_CONFIRM = (By.CSS_SELECTOR, u'#confirm>.ui-button-text') # x: 1135 y: 523 width: 59 height: 18, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None

    def click_button_confirm(self, wait_for_jquery=True):
        """
        Click button to confirm the dialog

        :param wait_for_jquery:  If true method waits for jquery
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_CONFIRM*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`, *timeout=60*
        """
        self.click_element(self.BUTTON_CONFIRM)
        if wait_for_jquery:
            self.wait_until_jquery_ajax_loaded(timeout=60)
