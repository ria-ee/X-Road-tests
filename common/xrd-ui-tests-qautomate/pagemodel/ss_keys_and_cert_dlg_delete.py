# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_keys_and_cert_dlg_delete(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160128112828
    # Pagemodel url: https://dev-ss1.palveluvayla.com:4000/keys
    # Pagemodel area: (538, 407, 846, 155)
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
    UI_ACTION_MAXIMIZE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-maximize') # x: 1279 y: 410 width: 51 height: 49
    UI_ACTION_CLOSE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-close') # x: 1330 y: 410 width: 51 height: 49
    TITLE = (By.ID, u'ui-id-8') # x: 550 y: 424 width: 162 height: 21
    DIALOG_CONTENT = (By.CSS_SELECTOR, u'div.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-dialog-buttons.ui-draggable.ui-resizable>#confirm') # x: 540 y: 461 width: 841 height: 52
    BUTTON_CANCEL = (By.CSS_SELECTOR, u'button.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-text-only') # x: 1202 y: 518 width: 77 height: 37
    BUTTON_CONFIRM = (By.CSS_SELECTOR, u'div.ui-dialog-buttonset>#confirm') # x: 1289 y: 518 width: 87 height: 37

    # @TODO is multible click confirm buttons nessecary?
    def click_delete_cert_confirm(self, text):
        """
        Click button to confirm certificate deletion

        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.BUTTON_CONFIRM*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_should_contain`, *self.DIALOG_CONTENT*, *key_confirm_delete*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_should_contain`, *self.DIALOG_CONTENT*, *key_confirm_key_name*
            * **Step 4:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_CONFIRM*
        """
        self.wait_until_element_is_visible(self.BUTTON_CONFIRM)
        key_confirm_delete = "Delete key"
        self.element_should_contain(self.DIALOG_CONTENT, key_confirm_delete)
        key_confirm_key_name = text
        self.element_should_contain(self.DIALOG_CONTENT, key_confirm_key_name)
        self.click_element(self.BUTTON_CONFIRM)
        sleep(1)

    def click_unregister_and_delete_cert_confirm(self, text):
        """
        Click button to confirm certificate deletion
        
        :param text:  String value for text
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.BUTTON_CONFIRM*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_should_contain`, *self.DIALOG_CONTENT*, *key_confirm_delete*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.element_should_contain`, *self.DIALOG_CONTENT*, *key_confirm_key_name*
            * **Step 4:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_CONFIRM*
        """
        self.wait_until_element_is_visible(self.BUTTON_CONFIRM)
        key_confirm_delete = "Key"
        self.element_should_contain(self.DIALOG_CONTENT, key_confirm_delete)
        key_confirm_key_name = text
        self.element_should_contain(self.DIALOG_CONTENT, key_confirm_key_name)
        self.click_element(self.BUTTON_CONFIRM)
        sleep(1)
