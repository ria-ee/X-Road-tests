# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_keys_and_cert_dlg_import_cert(CommonUtils):
    """

    """
    # Pagemodel timestamp: 20161107081755
    # Pagemodel url: https://test-ss1.i.palveluvayla.com:4000/keys
    # Pagemodel area: (609, 369, 706, 230)
    # Pagemodel screen resolution: (1920, 1080)
    # Use project settings: True
    # Used filters: id, css_selector, class_name, link_text, xpath
    # Xpath type: xpath-position
    # Depth of css path: 7
    # Minimize css selector: True
    # Create automated methods: True
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
    UI_ACTION_MAXIMIZE_SUBMIT = (By.CSS_SELECTOR, u'button.ui-action.ui-action-maximize') # x: 1208 y: 371 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    UI_ACTION_CLOSE_SUBMIT = (By.CSS_SELECTOR, u'button.ui-action.ui-action-close') # x: 1259 y: 371 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    TITLE = (By.ID, u'ui-id-1') # x: 620 y: 385 width: 124 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    SELECTED_FILE_TEXT = (By.CSS_SELECTOR, u'.selected_file') # x: 630 y: 441 width: 570 height: 33, tag: input, type: text, name: None, form_id: , checkbox: , table_id: 3, href:
    BUTTON_CANCEL = (By.CSS_SELECTOR, u'button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only') # x: 1173 y: 559 width: 77 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: , href:
    BUTTON_OK = (By.ID, u'file_upload_submit') # x: 1260 y: 559 width: 45 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: , href:

    # Dynamic objects:
    ID_FILE_UPLOAD_BUTTON = (By.ID, u'file_upload_button')     # x: 1207 y: 439 width: 83 height: 33 # Dynamic object

    def verify_title_file_dlg(self):
        """
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.BUTTON_OK*
        """
        self.wait_until_element_is_visible(self.BUTTON_OK)

    def click_browse_upload_button(self):
        """
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_FILE_UPLOAD_BUTTON*
        """
        self.click_element(self.ID_FILE_UPLOAD_BUTTON)

    def file_upload_ok(self):
        """
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_OK*
        """
        self.click_element(self.BUTTON_OK)
