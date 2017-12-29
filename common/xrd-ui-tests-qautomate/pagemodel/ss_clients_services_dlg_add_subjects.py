# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_clients_services_dlg_add_subjects(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20160902093138
    # Pagemodel url: https://xroad-lxd-ss1.lxd:4000/clients
    # Pagemodel area: (45, 133, 1830, 701)
    # Pagemodel screen resolution: (1920, 1080)
    # Use project settings: True
    # Used filters: id, css_selector, class_name, link_text, xpath
    # Xpath type: xpath-position
    # Depth of css path: 3
    # Minimize css selector: True
    # Create automated methods: True
    # Use css pattern: False
    # Allow non unique css pattern: False
    # Pagemodel template: False
    # Use testability: True
    # testability attribute: data-name
    # Use contains text in xpath: True
    # Exclude dynamic table filter: True
    # Row count: 2
    # Element count: 10
    # Big element filter width: 55
    # Big element filter height: 40
    # Not filtered elements: button, strong, select
    # Canvas modeling: False
    # Pagemodel type: normal
    # Links found: 0
    # Page model constants:
    MENUBAR_MAXIMIZE = (By.XPATH, u'//div[12]/div[1]/div[1]/button[1]') # x: 1770 y: 136 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: subjects, href:
    MENUBAR_CLOSE = (By.XPATH, u'//div[12]/div[1]/div[1]/button[2]') # x: 1821 y: 136 width: 51 height: 49, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: subjects, href:
    SIMPLE_SEARCH = (By.ID, u'ui-id-3') # x: 64 y: 202 width: 116 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    ADVANCED_SEARCH = (By.ID, u'ui-id-4') # x: 181 y: 202 width: 137 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: None
    ACL_SUBJECTS_SEARCH_SIMPLE_TAB_NAME_SUBJECT_ALL_TEXT = (By.CSS_SELECTOR, u'#acl_subjects_search_simple_search_tab>input[name="subject_search_all"]') # x: 78 y: 247 width: 179 height: 33, tag: input, type: text, name: subject_search_all, form_id: , checkbox: , table_id: , href:
    ACL_SUBJECTS_SEARCH_SIMPLE_TAB = (By.CSS_SELECTOR, u'#acl_subjects_search_simple_search_tab>.search') # x: 261 y: 247 width: 78 height: 33, tag: button, type: submit, name: None, form_id: , checkbox: , table_id: , href:
    ID = (By.XPATH, u'//div[12]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/table[1]/thead[1]/tr[1]/th[2]') # x: 960 y: 296 width: 896 height: 37, tag: th, type: , name: None, form_id: , checkbox: , table_id: subjects, href:
    BUTTON_CANCEL = (By.XPATH, u'//div[12]/div[3]/div[1]/button[4]') # x: 1471 y: 794 width: 77 height: 37, tag: button, type: button, name: cancel, form_id: , checkbox: , table_id: subjects, href:
    ID_ACL_SUBJECTS_SEARCH_ADD_ALL = (By.ID, u'acl_subjects_search_add_all') # x: 1557 y: 794 width: 130 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: , href:
    ID_ACL_SUBJECTS_SEARCH_ADD_SELECTED = (By.ID, u'acl_subjects_search_add_selected') # x: 1698 y: 794 width: 169 height: 37, tag: button, type: button, name: None, form_id: , checkbox: , table_id: , href:

    # Dynamic objects:
    ID_ACL_SUBJECTS_SEARCH = (By.ID, u'acl_subjects_search') # x: 64 y: 334 width: 1793 height: 63, tag: table, type: , name: None, form_id: , checkbox: , table_id: , href: # Dynamic object

    def verify_add_subjects_dlg_open(self):
        """
        Verify dialog is open

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.ID_ACL_SUBJECTS_SEARCH_ADD_ALL*
        """
        self.wait_until_element_is_visible(self.ID_ACL_SUBJECTS_SEARCH_ADD_ALL)

    def click_acl_subjects_add_to_acl(self):
        """
        Click button to add subject to acl

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_ACL_SUBJECTS_SEARCH_ADD_ALL*
        """
        self.click_element(self.ID_ACL_SUBJECTS_SEARCH_ADD_ALL)

    def click_search(self):
        """
        Click tab to search view
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ACL_SUBJECTS_SEARCH_SIMPLE_TAB*
        """
        self.click_element(self.ACL_SUBJECTS_SEARCH_SIMPLE_TAB)
        sleep(2)

    def click_and_open_subject(self):
        """
        Click subject from table with "Security server owners" text

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *element_rowtable[0]*
        """
        self.wait_until_jquery_ajax_loaded()
        element_rowtable = self.get_table_column_and_row_by_text_contains(self.ID_ACL_SUBJECTS_SEARCH, "Security server owners","TBODY/TR","TD")
        self.click_element(element_rowtable[0])

    def click_element_id_acl_subjects_search_add_selected(self):
        """

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_ACL_SUBJECTS_SEARCH_ADD_SELECTED*
        """
        self.click_element(self.ID_ACL_SUBJECTS_SEARCH_ADD_SELECTED)
