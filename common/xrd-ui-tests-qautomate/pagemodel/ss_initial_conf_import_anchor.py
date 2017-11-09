# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from common_lib.common_lib import Common_lib
from time import sleep

class Ss_initial_conf_import_anchor(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    common_lib = Common_lib()
    # Pagemodel timestamp: 20160330095200
    # Pagemodel url: https://test-rh1.i.palveluvayla.com:4000/init
    # Pagemodel area: Full screen
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
    ID_HEADING = (By.ID, u'heading') # x: 20 y: 14 width: 190 height: 22, tag: span, type: , name: None, form_id: , checkbox: , table_id: , href: None
    INIT_CONTAINER_IMPORT_CONFIGURATION_ANCHOR = (By.CSS_SELECTOR, u'#init-container>h2') # x: 610 y: 70 width: 700 height: 22, tag: h2, type: , name: None, form_id: , checkbox: , table_id: , href:
    TEXT = (By.XPATH, u'//section[1]/table[1]/tbody[1]/tr[1]/td[1]/input[1]') # x: 615 y: 97 width: 506 height: 33, tag: input, type: text, name: None, form_id: anchor_upload_form, checkbox: , table_id: 1, href:
    ID_ANCHOR_UPLOAD_SUBMIT = (By.ID, u'anchor_upload_submit') # x: 1215 y: 97 width: 78 height: 33, tag: button, type: submit, name: None, form_id: anchor_upload_form, checkbox: , table_id: 1, href:

    # Dynamic objects:
    CONTAINSCLASSSELECTED_FILE1 = (By.XPATH, u'(//*[contains(@class,\'selected_file\')])[1]')     # x: 615 y: 97 width: 506 height: 33 # Dynamic object
    ID_ANCHOR_UPLOAD_FILE_BUTTON = (By.ID, u'anchor_upload_file_button')     # x: 1129 y: 97 width: 83 height: 33 # Dynamic object

    def upload_anchor(self, parameters=None):
        """
        Upload anchor
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_ANCHOR_UPLOAD_FILE_BUTTON*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.common_lib`, *type_string*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_ANCHOR_UPLOAD_SUBMIT*
        """
        js = self.execute_javascript("document.querySelector('section.container>table.details>tbody>tr>td>input.selected_file').removeAttribute('disabled');")
        self.click_element(self.ID_ANCHOR_UPLOAD_FILE_BUTTON)
        sleep(3)
        import os
        import glob
        newest_anchor = max(glob.iglob(parameters[u'downloads_folder'] + '*.xml'), key=os.path.getctime)
        print(newest_anchor)
        file_name = newest_anchor
        type_string = file_name
        self.common_lib.type_file_name_pyautogui(type_string)
        print("done upload")
        sleep(2)
        enable_import = '$("#anchor_upload_submit").enable();'
        enable_import_js = "document.getElementById('anchor_upload_submit').removeAttribute('disabled');"
        js = self.execute_javascript(enable_import)
        self.click_element(self.ID_ANCHOR_UPLOAD_SUBMIT)
        sleep(3)

    def wait_until_element_is_visible_initial_conf(self):
        """
        Wait until initial confiquration view is visible

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.ID_HEADING*
        """
        self.wait_until_element_is_visible(self.ID_HEADING)

