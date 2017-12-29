# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_initial_conf_import_conf_dlg(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160330095307
    # Pagemodel url: https://xroad-lxd-ss1.lxd:4000/init
    # Pagemodel area: (585, 357, 754, 255)
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
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[1]') # x: 1233 y: 358 width: 51 height: 49, tag: button, type: submit, name: None, form_id: anchor_upload_form, checkbox: , table_id: 2, href: 
    MENUBAR_CLOSE = (By.XPATH, u'//div[7]/div[1]/div[1]/button[2]') # x: 1284 y: 358 width: 51 height: 49, tag: button, type: submit, name: None, form_id: anchor_upload_form, checkbox: , table_id: 2, href: 
    TITLE = (By.ID, u'ui-id-4') # x: 595 y: 373 width: 162 height: 21, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    HASH_SHA_224 = (By.XPATH, u'//div[2]/table[1]/tbody[1]/tr[1]/td[1]') # x: 600 y: 459 width: 118 height: 31, tag: td, type: , name: None, form_id: anchor_upload_form, checkbox: , table_id: 2, href: 
    CONST_07_AA_3E_F2_35_ED_E3_FA_4B_02 = (By.XPATH, u'//div[2]/table[1]/tbody[1]/tr[1]/td[2]') # x: 717 y: 459 width: 603 height: 31, tag: td, type: , name: None, form_id: anchor_upload_form, checkbox: , table_id: 2, href: 
    GENERATED = (By.XPATH, u'//div[2]/table[1]/tbody[1]/tr[2]/td[1]') # x: 600 y: 490 width: 118 height: 31, tag: td, type: , name: None, form_id: anchor_upload_form, checkbox: , table_id: 2, href: 
    CONST_00_2016_03_01_12_14_20 = (By.XPATH, u'//div[2]/table[1]/tbody[1]/tr[2]/td[2]') # x: 717 y: 490 width: 603 height: 31, tag: td, type: , name: None, form_id: anchor_upload_form, checkbox: , table_id: 2, href: 
    CANCEL = (By.XPATH, u'//div[7]/div[3]/div[1]/button[2]') # x: 1156 y: 569 width: 77 height: 37, tag: button, type: button, name: None, form_id: anchor_upload_form, checkbox: , table_id: 2, href: 
    BUTTON_CONFIRM = (By.CSS_SELECTOR, u'div.ui-dialog-buttonset>#confirm') # x: 1242 y: 569 width: 87 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: , href: 

    def click_button_ui_buttonset_confirm(self):
        """
        Click button to confirm dialog
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_CONFIRM*
        """
        # AutoGen method
        self.click_element(self.BUTTON_CONFIRM)

    def wait_until_element_is_visible_conf_required(self):
        """
        Wait until view is visible

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.TITLE*
        """
        self.wait_until_element_is_visible(self.TITLE)
