# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_client_dlg_details(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20151217124518
    # Pagemodel url: https://dev-ss1.palveluvayla.com:4000/clients
    # Pagemodel area: (558, 188, 801, 602)
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
    MENUBAR_MAXIMIZE = (By.CSS_SELECTOR, u'div[data-name="client_details_dialog"]>.ui-draggable-handle>.dialog-buttonbar>.ui-action-maximize') # x: 1258 y: 189 width: 51 height: 49
    MENUBAR_CLOSE = (By.CSS_SELECTOR, u'div[data-name="client_details_dialog"]>.ui-draggable-handle>.dialog-buttonbar>.ui-action-close') # x: 1309 y: 189 width: 51 height: 49
    ID_CLIENT_REGISTER = (By.ID, u'client_register') # x: 1040 y: 197 width: 89 height: 33
    ID_CLIENT_UNREGISTER = (By.ID, u'client_unregister') # x: 1132 y: 197 width: 111 height: 33
    UI_ID_13_XROAD_SUBSYSTEM_DEV_CS_PUB_ORG1_GUITEST = (By.CSS_SELECTOR, u'#ui-id-13>.xroad-id') # x: 638 y: 204 width: 298 height: 21
    DETAILS = (By.CSS_SELECTOR, u'#ui-id-14>.fa-info') # x: 676 y: 263 width: 5 height: 15
    SERVICE_CLIENTS = (By.CSS_SELECTOR, u'#ui-id-15>.fa-gears') # x: 753 y: 263 width: 16 height: 15
    SERVICES = (By.CSS_SELECTOR, u'#ui-id-16>.fa-wrench') # x: 892 y: 263 width: 14 height: 15
    INTERNAL_SEVERS = (By.CSS_SELECTOR, u'#ui-id-17>.fa-cloud') # x: 986 y: 263 width: 16 height: 15
    LOCAL_GROUPS = (By.CSS_SELECTOR, u'#ui-id-18>.fa-group') # x: 1135 y: 263 width: 16 height: 15
    ID_DETAILS_MEMBER_NAME = (By.ID, u'details_member_name') # x: 713 y: 315 width: 619 height: 33
    ID_DETAILS_MEMBER_CLASS = (By.ID, u'details_member_class') # x: 713 y: 358 width: 619 height: 33
    ID_DETAILS_MEMBER_CODE = (By.ID, u'details_member_code') # x: 713 y: 401 width: 619 height: 33
    ID_DETAILS_SUBSYSTEM_CODE = (By.ID, u'details_subsystem_code') # x: 713 y: 444 width: 619 height: 33
    TAB_CONTAINER_CERTIFICATES = (By.CSS_SELECTOR, u'#details_tab>section.container>h2>span') # x: 585 y: 499 width: 101 height: 22
    CERTIFICATES_WRAPPER_DATA_TABLES_SCROLL_HEAD_INNER_SORTING_ASC_CA = (By.CSS_SELECTOR, u'#certificates_wrapper>.dataTables_scroll>.dataTables_scrollHead>.dataTables_scrollHeadInner>.dataTable>thead>tr>.sorting_asc') # x: 586 y: 529 width: 187 height: 37
    CONTAINS_TEXT_SERIAL_NUMBER = (By.XPATH, u'//th[contains(text(),"Serial Number")]') # x: 773 y: 529 width: 187 height: 37
    CONTAINS_TEXT_STATE = (By.XPATH, u'//th[contains(text(),"State")]') # x: 960 y: 529 width: 187 height: 37
    CONTAINS_TEXT_EXPIRES = (By.XPATH, u'//th[contains(text(),"Expires")]') # x: 1147 y: 529 width: 187 height: 37
    BUTTON_CLOSE = (By.CSS_SELECTOR, u'div[data-name="client_details_dialog"]>.ui-dialog-buttonpane>.ui-dialog-buttonset>button[data-name="close"]') # x: 1288 y: 747 width: 67 height: 37

    def click_unregister_client(self):
        """
        Click button to unregister the client

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_CLIENT_DELETE*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.CLASS_UI_STATE_FOCUS*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_CLIENT_UNREGISTER*
        """
        sleep(1)
        #if self.is_visible(self.ID_CLIENT_DELETE,5):
        try:
            self.click_element(self.ID_CLIENT_DELETE)
            self.click_element(self.CLASS_UI_STATE_FOCUS)
        except:
            #sleep(2)
        #else:
            self.click_element(self.ID_CLIENT_UNREGISTER)