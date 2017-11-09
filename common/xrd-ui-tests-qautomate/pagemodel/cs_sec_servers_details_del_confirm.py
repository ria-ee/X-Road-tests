# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_sec_servers_details_del_confirm(CommonUtils):
    """

    """
    # Pagemodel timestamp: 20170206133035
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/securityservers
    # Pagemodel area: (614, 406, 691, 150)
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
    MENUBAR_CLOSE = (By.XPATH, u'//div[18]/div[1]/div[1]/button[2]') # x: 1254 y: 405 width: 51 height: 49, tag: button, type: submit, name: None, form_id: securityservers, checkbox: , table_id: securityserver_edit_table, href:
    TITLE = (By.ID, u'ui-id-17') # x: 625 y: 420 width: 167 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    DIALOG_CONTENT = (By.CSS_SELECTOR, u'div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-dialog-buttons.ui-draggable.ui-resizable>#confirm') # x: 615 y: 456 width: 691 height: 53, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href:
    BUTTON_CANCEL = (By.XPATH, u'//div[18]/div[3]/div[1]/button[2]') # x: 1130 y: 514 width: 75 height: 36, tag: button, type: button, name: None, form_id: securityservers, checkbox: , table_id: securityserver_edit_table, href:
    BUTTON_CONFIRM = (By.CSS_SELECTOR, u'div.ui-dialog-buttonset>#confirm') # x: 1215 y: 514 width: 85 height: 36, tag: button, type: button, name: None, form_id: , checkbox: , table_id: , href:

    def click_link_confirm_ui_text(self):
        """
        Click link to confirm dialog
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_CONFIRM*
        """
        # AutoGen method click_link: None
        self.click_element(self.BUTTON_CONFIRM)
