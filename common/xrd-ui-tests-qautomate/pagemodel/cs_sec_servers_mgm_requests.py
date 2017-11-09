# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Cs_sec_servers_mgm_requests(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20151215142413
    # Pagemodel url: https://dev-cs.palveluvayla.com:4000/securityservers
    # Pagemodel area: (458, 184, 1003, 604)
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
    UI_ACTION_MAXIMIZE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-maximize') # x: 1358 y: 184 width: 51 height: 49
    UI_ACTION_CLOSE = (By.CSS_SELECTOR, u'button.ui-action.ui-action-close') # x: 1409 y: 184 width: 51 height: 49
    TITLE = (By.ID, u'ui-id-3') # x: 470 y: 198 width: 159 height: 21
    SECURITY_SEVER_DETAILS = (By.ID, u'ui-id-4') # x: 650 y: 250 width: 173 height: 29
    CLIENTS = (By.ID, u'ui-id-5') # x: 824 y: 250 width: 66 height: 29
    AUTHENTICATION_CERTIFICATES = (By.ID, u'ui-id-6') # x: 891 y: 250 width: 201 height: 29
    MANAGEMENT_REQUESTS = (By.ID, u'ui-id-7') # x: 1093 y: 250 width: 177 height: 29
    ID_SECURITYSERVER_MANAGEMENT_REQUESTS_WRAPPER_REQUEST = (By.XPATH, u'id(\'securityserver_management_requests_wrapper\')/DIV[1]/DIV[1]/DIV[1]/TABLE[1]/THEAD[1]/TR[1]/TH[1]') # x: 486 y: 306 width: 237 height: 37
    ID_SECURITYSERVER_MANAGEMENT_REQUESTS_WRAPPER_REQUEST_TYPE = (By.XPATH, u'id(\'securityserver_management_requests_wrapper\')/DIV[1]/DIV[1]/DIV[1]/TABLE[1]/THEAD[1]/TR[1]/TH[2]') # x: 723 y: 306 width: 237 height: 37
    DATA_TABLES_SCROLL_HEAD_INNER_DISPLAY_SORTING_DESC_CREATED = (By.CSS_SELECTOR, u'div.dataTables_scrollHeadInner>table.display.dataTable>thead>tr>.sorting_desc') # x: 960 y: 306 width: 237 height: 37
    ID_SECURITYSERVER_MANAGEMENT_REQUESTS_WRAPPER_STATUS = (By.XPATH, u'id(\'securityserver_management_requests_wrapper\')/DIV[1]/DIV[1]/DIV[1]/TABLE[1]/THEAD[1]/TR[1]/TH[4]') # x: 1197 y: 306 width: 237 height: 37
    BUTTON_CLOSE = (By.CSS_SELECTOR, u'div.ui-dialog-buttonset>button[data-name="close"]') # x: 1388 y: 742 width: 67 height: 37

    # Dynamic objects:
    ID_SECURITYSERVER_MANAGEMENT_REQUESTS = (By.ID, u'securityserver_management_requests')     # x: 486 y: 345 width: 932 height: 1695 # Dynamic object

    def find_and_click_mgm_request(self):
        """
        Click management request in table with value "SUBMITTED FOR APPROVAL"
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
        """
        self.wait_until_jquery_ajax_loaded()
        element_rowtable = self.get_table_column_and_row_by_text(self.ID_SECURITYSERVER_MANAGEMENT_REQUESTS,"SUBMITTED FOR APPROVAL","TBODY/TR","TD")

        req_number = self.get_text(element_rowtable[0].find_elements(By.XPATH, "TD")[0])
        element_rowtable[0].find_element(By.LINK_TEXT, str(req_number)).click()
        #self.click_table_cell_by_column_and_row(self.ID_SECURITYSERVER_MANAGEMENT_REQUESTS,element_rowtable[2], element_rowtable[3])

    def click_close_mgm_req_dlg(self):
        """
        Click button to close the dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_CLOSE*
        """
        self.click_element(self.BUTTON_CLOSE)
