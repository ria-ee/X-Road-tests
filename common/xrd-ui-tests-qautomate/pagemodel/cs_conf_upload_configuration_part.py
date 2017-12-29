# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = self.get_current_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_conf_upload_configuration_part(CommonUtils):
    """

    """
    # Pagemodel timestamp: 20171220130401
    # Pagemodel url: https://xroad-lxd-cs.lxd:4000/configuration_management
    # Pagemodel area: (611, 376, 700, 233)
    # Pagemodel screen resolution: (5760, 1080)
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
    SUBMIT_0 = (By.XPATH, u'//div[4]/div[1]/div[1]/button[1]') # x: 1208 y: 376 width: 51 height: 49, tag: button, type: submit, name: None, form_id: upload_conf_part, checkbox: , table_id: 5, href:
    DATA_NAME_FILE_UPLOAD_UI_RESIZABLE_E = (By.CSS_SELECTOR, u'div[data-name="file_upload_dialog"]>.ui-resizable-e') # x: 1308 y: 376 width: 7 height: 230, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href:
    UNKNOWN_0 = (By.XPATH, u'//div[4]/div[1]/div[1]/button[1]/i[1]') # x: 1224 y: 390 width: 21 height: 21, tag: i, type: , name: None, form_id: upload_conf_part, checkbox: , table_id: 5, href:
    ID_UI_ID_1 = (By.ID, u'ui-id-1') # x: 620 y: 391 width: 190 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    DEVICE_ID_KEY = (By.XPATH, u'//div[3]/div[2]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[1]') # x: 301 y: 422 width: 1306 height: 37, tag: th, type: , name: None, form_id: upload_conf_part, checkbox: , table_id: 5, href:
    SELECTED_FILE_TEXT = (By.CSS_SELECTOR, u'.selected_file') # x: 630 y: 447 width: 569 height: 32, tag: input, type: text, name: None, form_id: , checkbox: , table_id: 5, href:
    ID_FILE_UPLOAD_SUBMIT = (By.ID, u'file_upload_submit') # x: 1261 y: 565 width: 44 height: 36, tag: button, type: button, name: ok, form_id: , checkbox: , table_id: , href:
    OK = (By.XPATH, u'//div[4]/div[3]/div[1]/button[1]/span[1]') # x: 1274 y: 574 width: 18 height: 18, tag: span, type: , name: None, form_id: upload_conf_part, checkbox: , table_id: 5, href: None
    DATA_NAME_FILE_UPLOAD_UI_ICON_GRIPSMALL_DIAGONAL_SE = (By.CSS_SELECTOR, u'div[data-name="file_upload_dialog"]>.ui-icon-gripsmall-diagonal-se') # x: 1303 y: 599 width: 12 height: 12, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href:
    DATA_NAME_FILE_UPLOAD_UI_RESIZABLE = (By.CSS_SELECTOR, u'div[data-name="file_upload_dialog"]>.ui-resizable-s') # x: 610 y: 604 width: 700 height: 7, tag: div, type: , name: None, form_id: , checkbox: , table_id: , href:

    # Dynamic objects:
    FILE_UPLOAD_BUTTON = (By.ID, u'file_upload_button') # x: 1206 y: 446 width: 84 height: 33, tag: label, type: , name: None, form_id: , checkbox: , table_id: , href:
    CANCEL = (By.XPATH, u'(//*[contains(@data-name,\'cancel\')])[1]') # x: 1176 y: 565 width: 75 height: 36, tag: button, type: button, name: cancel, form_id: , checkbox: , table_id: , href: 

    def click_browse(self):
        """
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.FILE_UPLOAD_BUTTON*
        """
        self.click_element(self.FILE_UPLOAD_BUTTON)

    def click_ok(self):
        """
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_FILE_UPLOAD_SUBMIT*
        """
        self.click_element(self.ID_FILE_UPLOAD_SUBMIT)

    def click_close(self):
        """
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.CANCEL*
        """
        self.click_element(self.CANCEL)
