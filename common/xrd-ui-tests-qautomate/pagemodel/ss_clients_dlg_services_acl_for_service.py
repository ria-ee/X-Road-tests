# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_clients_dlg_services_acl_for_service(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20151210141122
    # Pagemodel url: https://dev-ss1.palveluvayla.com:4000/clients
    # Pagemodel area: (47, 237, 1826, 495)
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
    # Row count: 25
    # Element count: 140
    # Big element filter width: 55
    # Big element filter height: 40
    # Not filtered elements: button, strong, select
    # Canvas modeling: False
    # Pagemodel type: normal
    # Links found: 0
    # Page model constants:
    MENUBAR_MAXIMIZE = (By.CSS_SELECTOR, u'div[data-name="service_acl_dialog"]>.ui-draggable-handle>.dialog-buttonbar>.ui-action-maximize') # x: 1770 y: 240 width: 51 height: 49
    ID_SERVICE = (By.ID, u'service') # x: 125 y: 315 width: 135 height: 35
    SIMPLE_SEARCH = (By.ID, u'ui-id-5') # x: 64 y: 361 width: 116 height: 29
    ADVANCED_SEARCH = (By.ID, u'ui-id-6') # x: 181 y: 361 width: 137 height: 29
    SUBJECTS_SIMPLE_SEARCH_TAB_NAME_SUBJECT_ALL = (By.CSS_SELECTOR, u'#subjects_simple_search_tab>input[name="subject_search_all"]') # x: 78 y: 406 width: 179 height: 33
    SUBJECTS_SIMPLE_SEARCH_TAB = (By.CSS_SELECTOR, u'#subjects_simple_search_tab>.search') # x: 261 y: 406 width: 78 height: 33
    SUBJECTS_WRAPPER_DATA_TABLES_SCROLL_HEAD_INNER_SORTING_ASC_MEMBER = (By.CSS_SELECTOR, u'#subjects_wrapper>.dataTables_scroll>.dataTables_scrollHead>.dataTables_scrollHeadInner>.dataTable>thead>tr>.sorting_asc') # x: 64 y: 455 width: 757 height: 37
    ID_SUBJECTS_WRAPPER = (By.XPATH, u'id(\'subjects_wrapper\')/DIV[1]/DIV[1]/DIV[1]/TABLE[1]/THEAD[1]/TR[1]/TH[2]') # x: 821 y: 455 width: 757 height: 37
    ID_SUBJECTS_WRAPPER_ACCESS_RIGHTS_GIVEN = (By.XPATH, u'id(\'subjects_wrapper\')/DIV[1]/DIV[1]/DIV[1]/TABLE[1]/THEAD[1]/TR[1]/TH[3]') # x: 1578 y: 455 width: 279 height: 37
    SUBJECTS_ODD_DATA_TABLES_EMPTY_NO_MATCHING_RECORDS = (By.CSS_SELECTOR, u'#subjects>tbody>.odd>.dataTables_empty') # x: 64 y: 493 width: 1793 height: 31
    ID_SERVICE_ACL_SUBJECTS_ADD = (By.ID, u'service_acl_subjects_add') # x: 1398 y: 688 width: 119 height: 37
    ID_SERVICE_ACL_SUBJECTS_REMOVE_SELECTED = (By.ID, u'service_acl_subjects_remove_selected') # x: 1527 y: 688 width: 146 height: 37
    ID_SERVICE_ACL_SUBJECTS_REMOVE_ALL = (By.ID, u'service_acl_subjects_remove_all') # x: 1683 y: 688 width: 107 height: 37
    DATA_NAME_SERVICE_ACL_UI_BUTTONPANE_BUTTONSET_CLOSE = (By.CSS_SELECTOR, u'div[data-name="service_acl_dialog"]>.ui-dialog-buttonpane>.ui-dialog-buttonset>button[data-name="close"]') # x: 1800 y: 688 width: 67 height: 37

    def verify_acl_dlg_open(self):
        """
        Verify acl dialog is open

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.MENUBAR_MAXIMIZE*
        """
        self.wait_until_element_is_visible(self.MENUBAR_MAXIMIZE)

    def click_acl_subjects_add(self):
        """
        Click button to add scl subject

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_SERVICE_ACL_SUBJECTS_ADD*
        """
        self.click_element(self.ID_SERVICE_ACL_SUBJECTS_ADD)

    def click_close_dlg_acl(self):
        """
        Click button to close the dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DATA_NAME_SERVICE_ACL_UI_BUTTONPANE_BUTTONSET_CLOSE*
        """
        self.click_element(self.DATA_NAME_SERVICE_ACL_UI_BUTTONPANE_BUTTONSET_CLOSE)