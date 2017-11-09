# -*- coding: utf-8 -*-
# Example for using WebDriver object: driver = get_driver() e.g driver.current_url
from webframework import TESTDATA
from selenium.webdriver.common.by import By
from webframework.extension.util.common_utils import *
from webframework.extension.util.webtimings import get_measurements
from webframework.extension.parsers.parameter_parser import get_parameter
from time import sleep

class Ss_clients_dlg_services(CommonUtils):
    """
    Pagemodel

    Changelog:

    * 27.07.2017
        | Docstrings updated
    """
    # Pagemodel timestamp: 20151211081433
    # Pagemodel url: https://dev-ss1.palveluvayla.com:4000/clients
    # Pagemodel area: (559, 186, 802, 603)
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
    MENUBAR_MAXIMIZE = (By.CSS_SELECTOR, u'div[data-name="client_details_dialog"]>.ui-draggable-handle>.dialog-buttonbar>.ui-action-maximize') # x: 1258 y: 185 width: 51 height: 49
    MENUBAR_CLOSE = (By.CSS_SELECTOR, u'div[data-name="client_details_dialog"]>.ui-draggable-handle>.dialog-buttonbar>.ui-action-close') # x: 1309 y: 185 width: 51 height: 49
    SERVICE_CLIENTS = (By.CSS_SELECTOR, u'#ui-id-15>.fa-gears') # x: 753 y: 259 width: 16 height: 15
    SERVICES = (By.CSS_SELECTOR, u'#ui-id-16>.fa-wrench') # x: 892 y: 259 width: 14 height: 15
    INTERNAL_SERVERS = (By.CSS_SELECTOR, u'#ui-id-17>.fa-cloud') # x: 986 y: 259 width: 16 height: 15
    LOCAL_GROUPS = (By.CSS_SELECTOR, u'#ui-id-18>.fa-group') # x: 1135 y: 259 width: 16 height: 15
    SERVICES_FILTER = (By.CSS_SELECTOR, u'#services_filter>label>input') # x: 631 y: 302 width: 179 height: 33
    ID_WSDL_ADD = (By.ID, u'wsdl_add') # x: 581 y: 340 width: 77 height: 28
    ID_WSDL_ENABLE = (By.ID, u'wsdl_enable') # x: 662 y: 340 width: 62 height: 28
    ID_WSDL_REFRESH = (By.ID, u'wsdl_refresh') # x: 727 y: 340 width: 67 height: 28
    ID_WSDL_DELETE = (By.ID, u'wsdl_delete') # x: 798 y: 340 width: 60 height: 28
    ID_SERVICE_PARAMS = (By.ID, u'service_params') # x: 862 y: 340 width: 45 height: 28
    ID_SERVICE_ACL = (By.ID, u'service_acl') # x: 911 y: 340 width: 100 height: 28
    ID_SERVICES_WRAPPER_SERVICE = (By.XPATH, u'id(\'services_wrapper\')/DIV[2]/DIV[1]/DIV[1]/TABLE[1]/THEAD[1]/TR[1]/TH[2]') # x: 592 y: 374 width: 199 height: 54
    ID_SERVICES_WRAPPER_TITLE = (By.XPATH, u'id(\'services_wrapper\')/DIV[2]/DIV[1]/DIV[1]/TABLE[1]/THEAD[1]/TR[1]/TH[3]') # x: 791 y: 374 width: 199 height: 54
    CONTAINS_TEXT_URL = (By.XPATH, u'//th[contains(text(),"URL")]') # x: 990 y: 374 width: 199 height: 54
    CONTAINS_TEXT_TIMEOUT = (By.XPATH, u'//th[contains(text(),"Timeout (s)")]') # x: 1189 y: 374 width: 59 height: 54
    CONTAINS_TEXT_LAST_REFRESHED = (By.XPATH, u'//th[contains(text(),"Last Refreshed")]') # x: 1248 y: 374 width: 96 height: 54
    OPEN = (By.CSS_SELECTOR, u'.open') # x: 576 y: 429 width: 16 height: 32
    BUTTON_CLOSE = (By.CSS_SELECTOR, u'div[data-name="client_details_dialog"]>.ui-dialog-buttonpane>.ui-dialog-buttonset>button[data-name="close"]') # x: 1288 y: 743 width: 67 height: 37

    # Dynamic objects:
    DETAILS_TAB = (By.LINK_TEXT, u'Details') # x: 664 y: 194 width: 76 height: 29, tag: a, type: , name: None, form_id: , checkbox: , table_id: , href: https://xroad-lxd-ss1.lxd:4000/clients#details_tab
    ID_SERVICES = (By.ID, u'services')     # x: 576 y: 429 width: 769 height: 31 # Dynamic object
    CLASS_CLOSED = (By.CLASS_NAME, u'closed')     # x: 576 y: 429 width: 16 height: 31 # Dynamic object
    CONTAINSTEXTWSDLDISABLED = (By.XPATH, u'//*[contains(text(),\'WSDL DISABLED\')]')     # x: 592 y: 429 width: 597 height: 52 # Dynamic object

    def verify_client_dlg_open(self):
        """
        Verify that clients services dialog is open

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_element_is_visible`, *self.MENUBAR_MAXIMIZE*
        """
        self.wait_until_element_is_visible(self.MENUBAR_MAXIMIZE)

    def click_wsdl_add(self):
        """
        Click button to add wsdl

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_WSDL_ADD*
        """
        self.click_element(self.ID_WSDL_ADD)

    def open_wsdl_service(self):
        """
        Click button to upen wsdl services
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.CLASS_CLOSED*
        """
        self.click_element(self.CLASS_CLOSED)

    def click_and_open_wsdl_service(self, parameters=None):
        """
        Click and open wsdl service with parameter 'service_name'
        
        :param parameters:  Test data section dictionary
        
        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_jquery_ajax_loaded`
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.wait_until_page_contains`, *parameters[u'service_name_short']*
            * **Step 3:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *element_rowtable[0]*
            * **Step 4:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.SERVICES_FILTER*
            * **Step 5:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *element_rowtable[1]*
        """
        self.wait_until_jquery_ajax_loaded()
        self.wait_until_page_contains(parameters[u'service_name_short'])
        element_rowtable = self.get_table_column_and_row_by_text(self.ID_SERVICES, parameters[u'service_name'],"TBODY/TR","TD")
        self.click_element(element_rowtable[0])
        self.click_element(self.SERVICES_FILTER)
        sleep(1)
        self.click_element(element_rowtable[1])
        sleep(1)

    def click_edit_service_params(self):
        """
        Click button to edit service parameters

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_SERVICE_PARAMS*
        """
        self.click_element(self.ID_SERVICE_PARAMS)

    def click_services_access_rights(self):
        """
        Click button to services access rights

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_SERVICE_ACL*
        """
        self.click_element(self.ID_SERVICE_ACL)

    def click_wsdl_enable(self):
        """
        Click button to enable wsdl

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.CONTAINSTEXTWSDLDISABLED*
            * **Step 2:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.ID_WSDL_ENABLE*
        """
        self.click_element(self.CONTAINSTEXTWSDLDISABLED)
        self.click_element(self.ID_WSDL_ENABLE)

    def click_close_services_dlg(self):
        """
        Click button to close the dialog

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.BUTTON_CLOSE*
        """
        self.click_element(self.BUTTON_CLOSE)

    def click_element_details_tab(self):
        """
        Click tab to open details tab

        **Test steps:**
            * **Step 1:** :func:`~webframework.extension.util.common_utils.CommonUtils.click_element`, *self.DETAILS_TAB*
        """
        self.click_element(self.DETAILS_TAB)
